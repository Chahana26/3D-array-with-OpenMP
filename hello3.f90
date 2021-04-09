module code
        contains
subroutine printing(i,j,Q,s)
   real(kind=8), intent(inout):: Q(2,2,2)
   integer, intent (in) :: i,j
   integer :: k
   real :: a
   real, intent(inout) :: s(2,2)
   a = 0
   DO k = 1,2
      a = a + Q(i,j,k)
   END DO
   s(i,j) = a
   return

end subroutine printing
end module code
