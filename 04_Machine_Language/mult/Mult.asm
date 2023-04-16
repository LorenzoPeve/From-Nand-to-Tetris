// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// BASECASE Address R0 or R1 equal to zero
@R0
D=M
@BASECASE
D; JEQ

@R1
D=M
@BASECASE
D; JEQ

// 1. Initialize leftoperand = RAM[0], i = RAM[1], and R2 = 0
@R0
D=M
@leftoperand     	// address 16
M=D

@R1
D=M
@i          			// address 17
M=D

@R2					// address 18
M=0

// 2. Loop

(LOOP)
	// if (i==0) go to END
	@i
	D=M
	@END
	D; JEQ

	@R2
	D=M
	@leftoperand
	D=D+M
	@R2
	M=D

	// i--
	@i
	M=M-1

	@LOOP
	0; JMP

(BASECASE)
	@R2
	M=0

(END)
	@END
	0; JMP
