import multi
import numpy as np
from cffi import FFI
ffi = FFI()


def convert_to_from_cffi(c_or_numpy_array, num_bytes=None):

        '''
        Utility function to convert to and from numpy and ffi buffer interfaces
        Args:
            c_or_numpy_array (buffer):
                an object that is either a numpy array or a FFI cdata pointer
            num_bytes (integer, optional):
                size of buffer when converting from CFFI to ndarray
        '''

        if isinstance(c_or_numpy_array, np.ndarray):
            out_buffer = ffi.cast('{} *'.format('double'),
                                        c_or_numpy_array.ctypes.data)
        elif isinstance(c_or_numpy_array, ffi.CData):
            out_buffer = np.frombuffer(ffi.buffer(
                c_or_numpy_array, num_bytes), dtype=np.float64)
        else:
            raise ValueError(
                'Buffer must be either numpy.ndarray or ffi CData,\
                not {}'.format(type(c_or_numpy_array)))

        return out_buffer

new = np.random.rand(2,2,2)
print(new)
multi.lib.printm(convert_to_from_cffi(new))
