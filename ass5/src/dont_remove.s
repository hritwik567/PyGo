.section .text
.globl main

main:
call _func_main
push $0
call exit

_func_foo:
push %ebp
movl %esp, %ebp
sub $0, %esp
movl 0(%ebp), %eax
addl 4(%ebp), %eax
movl %ebp, %esp
pop %ebp
ret

movl %ebp, %esp
pop %ebp
ret

_func_main:
push %ebp
movl %esp, %ebp
sub $12, %esp
push $2
push $1
call _func_foo
addl $8, %esp
movl %eax, %edx
movl $3, %eax
movl %eax, -8(%ebp)
movl %edx, -4(%ebp)
movl %eax, %ebx
movl -8(%ebp), %eax
imul %ebx, %eax
movl %edx, -4(%ebp)
push %eax
push $2
push $1
call _func_foo
addl $8, %esp
pop %edx
imul -8(%ebp), %eax
movl %eax, %ebx
movl %edx, %eax
addl %ebx, %eax
movl %eax, -12(%ebp)
movl %ebp, %esp
pop %ebp
ret


.section .data
