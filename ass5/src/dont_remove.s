.section .text
.globl main

main:
call _func_main
push $0
call exit

_func_main:
push %ebp
movl %esp, %ebp
subl $16, %esp
movl $3, %eax
movl %eax, %edx
movl $4, %eax
movl %edx, -4(%ebp)
movl %eax, %edx
movl $5, %eax
movl %eax, -12(%ebp)
movl %edx, -8(%ebp)
movl -4(%ebp), %eax
addl $1, %eax
movl %eax, -16(%ebp)
movl %edx, -8(%ebp)
movl %ebp, %esp
pop %ebp
ret

.section .data
