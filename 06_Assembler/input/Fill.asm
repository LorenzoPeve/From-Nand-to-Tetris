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


(LISTEN_KEYBOARD)
@KBD
D=M
@KEYBOARD_PRESSED
D; JGT
@pixel_fill
M=0
@INITIALIZE
0; JMP

(KEYBOARD_PRESSED)
@pixel_fill
M=-1

(INITIALIZE)
// INITIALIZE `row_idx` = `col_idx` = 0. We need to loop over all rows and cols.
@R0
D=A
@row_idx
M=D

@R0
D=A
@col_idx
M=D

// INITIALIZE `screen_register`=0. This is HOW we are going to change pixels
// Why? (1) We cannot address single bits, so we cannot do arr[row, col]
@SCREEN
D=A
@screen_register // 0 to 8191
M=D

// INITIALIZE `ROW_MAX`=256 `COL_MAX`=32. This is to
@256
D=A
@ROW_MAX
M=D

@32
D=A
@COL_MAX
M=D

(LOOP_ROWS)
  // if (i==256) go to LOOP_ROWS (i.e., next row)
  @row_idx
  D=M
  @ROW_MAX
  D=M-D
  @END
  D; JEQ

  // Reset column counter
  @col_idx
  M=0

  // i++
  @row_idx
  M=M+1

  @LOOP_COLUMNS
  0; JMP


(LOOP_COLUMNS) // Fills a row from left to right
  // if (i==32) go to LOOP_ROWS (i.e., next row)
  @col_idx
  D=M
  @COL_MAX
  D=M-D
  @LOOP_ROWS
  D; JEQ

  // Setting RAM[screen_register] = pixel_fill
  @pixel_fill
  D=M
  @screen_register
  A=M
  M=D

  // screen_register++
  @screen_register
  M=M+1

  // col_idx++
  @col_idx
  M=M+1

  @LOOP_COLUMNS
	0; JMP

(END)
  @LISTEN_KEYBOARD
  0; JMP
