// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Define constants
@8191
D=A
@current_register
M=D

(LISTEN_KEYBOARD)
@KBD
D=M
@FILL_LOOP
D; JGT
@UNFILL_LOOP
0;JMP

(FILL_LOOP)
    @SCREEN
    D=A
    @current_register   // Screen register 100
    A=D+M               // 16384 + 100
    M=-1

    @current_register
    MD=M-1
    @RESET
    D; JLT
    @FILL_LOOP
    0; JMP

(UNFILL_LOOP)
    @SCREEN
    D=A
    @current_register
    A=D+M
    M=0

    @current_register
    MD=M-1
    @RESET
    D; JLT
    @UNFILL_LOOP
    0; JMP


(RESET)
@8191
D=A
@current_register
M=D
@LISTEN_KEYBOARD
0; JMP
