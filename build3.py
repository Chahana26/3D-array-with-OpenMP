import os
import numpy as np
from cffi import FFI
from os.path import abspath

desired_compiler = 'gcc'
real2_library_path = abspath('./libmularray.a')

absolute_library_path = os.path.abspath(real2_library_path)


def as_pointer(numpy_array):
    assert numpy_array.flags['F_CONTIGUOUS'], \
        "array is not contiguous in memory (Fortran order)"
    return ffi.cast("double*", numpy_array.__array_interface__['data'][0])


def convert_to_from_cffi(self, c_or_numpy_array, num_bytes=None):

        '''
        Utility function to convert to and from numpy and ffi buffer interfaces
        Args:
            c_or_numpy_array (buffer):
                an object that is either a numpy array or a FFI cdata pointer
            num_bytes (integer, optional):
                size of buffer when converting from CFFI to ndarray
        '''

        if isinstance(c_or_numpy_array, np.ndarray):
            out_buffer = self._ffi.cast('{} *'.format(self._ffi_type),
                                        c_or_numpy_array.ctypes.data)
        elif isinstance(c_or_numpy_array, self._ffi.CData):
            out_buffer = np.frombuffer(self._ffi.buffer(
                c_or_numpy_array, num_bytes), dtype=self._numpy_type)
        else:
            raise ValueError(
                'Buffer must be either numpy.ndarray or ffi CData,\
                not {}'.format(type(c_or_numpy_array)))

        return out_buffer



####################
# Setup part
####################

if not os.environ.get('CC'):
    os.environ['CC'] = desired_compiler


####################
# Compilation part
####################

ffibuilder = FFI()
# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
ffibuilder.cdef("void printm(double *Q);", override=True)


# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.  This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
ffibuilder.set_source("multi",''' #include "extra3.h" ''',
                      library_dirs=[os.getcwd()],
                      include_dirs=[os.getcwd()],
                      extra_link_args=[os.path.abspath(real2_library_path), '-lgfortran',])
ffibuilder.compile(verbose=True)
