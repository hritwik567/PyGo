.section .text
.globl main

main:
call _func_main
push $0
call exit

_func_main:
push %ebp
movl %esp, %ebp
sub $96, %esp
lea -96(%ebp), %eax
movl %eax, %edx
movl $0, %eax
movl %eax, %ebx
movl %edx, %eax
addl %ebx, %eax
movl %eax, %edx
movl $1, %eax
movl %eax, %ebx
movl %edx, %eax
addl %ebx, %eax
movl %eax, %edx
movl $2, %eax
movl %eax, %ebx
movl %edx, %eax
addl %ebx, %eax
movl %eax, %edi
movl $3, (%edi)
movl %ebp, %esp
pop %ebp
ret


.section .data
