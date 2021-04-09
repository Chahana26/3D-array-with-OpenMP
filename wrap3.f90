module wrapper
        use iso_c_binding, only: c_int, c_double
        use code, only: printing
        USE OMP_LIB
        implicit none

        contains

                subroutine printm(Q) bind(c)
                 real(c_double), intent(inout) :: Q(2,2,2)
                 real :: s(2,2)
                 integer :: i,j
                 real :: total_sum

                 !$OMP PARALLEL  SHARED(total_Sum)

                     DO i = 1,2
                        Do j = 1,2
                           s(i,j) = 0
                        End do
                     end do
                     total_Sum = 0;


                     DO i=1,2
                        DO j = 1,2
                           call printing(i,j,Q,s)
                        END DO
                     END DO

                     print*,'the array after addition along 1 directions looks like this:'
                     print*, 'trying to print row-wise'
                     do i = 1, ubound(s, 2)
                        print *, s(:,i)
                     end do
                     !$OMP CRITICAL
                        DO i=1,2
                           DO j = 1,2
                              total_Sum = total_Sum + s(i,j)
                           END DO
                        END DO
                     !$OMP END CRITICAL
                 !$OMP END PARALLEL
                 print*,'total sum is',total_sum
                end subroutine printm

end module
