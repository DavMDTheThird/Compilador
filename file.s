.data
	newline: .asciiz "\n"

.text
.globl main
main:
	
# Setup main's stack frame
	subu $sp, $sp, 4
	sw $fp, ($sp)
	move $fp, $sp
	li $t0, 0
	li $t1, -20
	add $t1, $t1, $fp
	li $t2, 5
	L0:
	sw $t0, ($t1)
	addi $t1, $t1, 4
	addi $t2, $t2, -1
	bgtz $t2, L0
	sw $zero, -24($fp)
	subu $sp, $sp, 24
	
# Loading constant 0
	li $t3, 0
	
# Loading constant 0
	li $t4, 0
	sw $t4, -24($fp)
	
L1:
	
# Loading i
	lw $t5, -24($fp)
	
# Loading constant 5
	li $t6, 5
	slt $t7, $t5, $t6
	beq $t7, $zero, L2
	j L1
	L2:
	
# Cleanup main's stack frame
	move $sp, $fp
	lw $fp, ($sp)
	addu $sp, $sp, 4
	
# Exit program
	li $v0, 10
	syscall
