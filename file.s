.data
	newline: .asciiz "\n"

.text
.globl main
main:
	
# Setup main's stack frame
	subu $sp, $sp, 4
	sw $fp, ($sp)
	move $fp, $sp
	sw $zero, -4($fp)
	sw $zero, -8($fp)
	sw $zero, -12($fp)
	subu $sp, $sp, 12
	
# Reading input from user
	li $v0, 5
	syscall
	sw $v0, -4($fp)
	
# Reading input from user
	li $v0, 5
	syscall
	sw $v0, -8($fp)
	
# Loading x
	lw $t0, -4($fp)
	
# Loading y
	lw $t1, -8($fp)
	
# Arithmetic operation: *
	mul $t2, $t0, $t1
	
# Loading x
	lw $t3, -4($fp)
	
# Loading y
	lw $t4, -8($fp)
	
# Arithmetic operation: *
	mul $t5, $t3, $t4
	sw $t5, -12($fp)
	
# Loading sum
	lw $t6, -12($fp)
	
# Loading sum
	lw $t7, -12($fp)
	move $a0, $t7
	li $v0, 1
	syscall
	li $v0, 4
	la $a0, newline
	syscall
	
# Cleanup main's stack frame
	move $sp, $fp
	lw $fp, ($sp)
	addu $sp, $sp, 4
	
# Exit program
	li $v0, 10
	syscall
