// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Retrieve R0; check if zero; set "left_operand" for convenience
@R0
D=M
@BASE_CASE_ZERO
D; JEQ 
@left_operand
M=D

// Retrieve R1; check if zero; set "right_operand" for convenience
@R1
D=M
@BASE_CASE_ZERO
D; JEQ
@right_operand
M=D

// Initialize iteration parameters
// Iteration wil do i-- until reaching zero
@sum
M=0
@right_operand
D=M
@iteration_n
M=D

(ADD_LOOP)
@left_operand
D=M
@sum
M=D+M

// If n is zero, end iteration
@iteration_n
MD=M-1
@RESULT
D;JEQ

// else, goto ADD_LOOP
@ADD_LOOP
0;JMP

(RESULT)
@sum
D=M
@R2
M=D
@END
0; JMP

(BASE_CASE_ZERO)
@R2
M=0

(END)
@END
0; JMP
