@17
D=A
@0
A=M
M=D
@0
M=M+1
@17
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@R14
D=D-M
@IS_EQUAL_1
D; JEQ
@R15
M=0
@PUT_RESULT_IN_STACK_1
0; JMP
(IS_EQUAL_1)
@R15
M=-1
(PUT_RESULT_IN_STACK_1)
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@17
D=A
@0
A=M
M=D
@0
M=M+1
@16
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@R14
D=D-M
@IS_EQUAL_2
D; JEQ
@R15
M=0
@PUT_RESULT_IN_STACK_2
0; JMP
(IS_EQUAL_2)
@R15
M=-1
(PUT_RESULT_IN_STACK_2)
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@16
D=A
@0
A=M
M=D
@0
M=M+1
@17
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@R14
D=D-M
@IS_EQUAL_3
D; JEQ
@R15
M=0
@PUT_RESULT_IN_STACK_3
0; JMP
(IS_EQUAL_3)
@R15
M=-1
(PUT_RESULT_IN_STACK_3)
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@892
D=A
@0
A=M
M=D
@0
M=M+1
@891
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@X_GT_EQ_THAN_ZERO4
D; JGE
@X_LESS_THAN_ZERO4
0; JMP
(X_GT_EQ_THAN_ZERO4)
@R14
D=M
@SAME_SIGN4
D; JGE
@IS_FALSE_4
0; JMP
(X_LESS_THAN_ZERO4)
@R14
D=M
@SAME_SIGN4
D; JLT
@IS_TRUE_4
0; JMP
(SAME_SIGN4)
@R13
D=M
@R14
D=D-M
@IS_TRUE_4
D; JLT
@IS_FALSE_4
0; JMP
(IS_TRUE_4)
@R15
M=-1
@PUT_RESULT_IN_STACK_4
0; JMP
(IS_FALSE_4)
@R15
M=0
@PUT_RESULT_IN_STACK_4
0; JMP
(PUT_RESULT_IN_STACK_4)
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@891
D=A
@0
A=M
M=D
@0
M=M+1
@892
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@X_GT_EQ_THAN_ZERO5
D; JGE
@X_LESS_THAN_ZERO5
0; JMP
(X_GT_EQ_THAN_ZERO5)
@R14
D=M
@SAME_SIGN5
D; JGE
@IS_FALSE_5
0; JMP
(X_LESS_THAN_ZERO5)
@R14
D=M
@SAME_SIGN5
D; JLT
@IS_TRUE_5
0; JMP
(SAME_SIGN5)
@R13
D=M
@R14
D=D-M
@IS_TRUE_5
D; JLT
@IS_FALSE_5
0; JMP
(IS_TRUE_5)
@R15
M=-1
@PUT_RESULT_IN_STACK_5
0; JMP
(IS_FALSE_5)
@R15
M=0
@PUT_RESULT_IN_STACK_5
0; JMP
(PUT_RESULT_IN_STACK_5)
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@891
D=A
@0
A=M
M=D
@0
M=M+1
@891
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@X_GT_EQ_THAN_ZERO6
D; JGE
@X_LESS_THAN_ZERO6
0; JMP
(X_GT_EQ_THAN_ZERO6)
@R14
D=M
@SAME_SIGN6
D; JGE
@IS_FALSE_6
0; JMP
(X_LESS_THAN_ZERO6)
@R14
D=M
@SAME_SIGN6
D; JLT
@IS_TRUE_6
0; JMP
(SAME_SIGN6)
@R13
D=M
@R14
D=D-M
@IS_TRUE_6
D; JLT
@IS_FALSE_6
0; JMP
(IS_TRUE_6)
@R15
M=-1
@PUT_RESULT_IN_STACK_6
0; JMP
(IS_FALSE_6)
@R15
M=0
@PUT_RESULT_IN_STACK_6
0; JMP
(PUT_RESULT_IN_STACK_6)
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@32767
D=A
@0
A=M
M=D
@0
M=M+1
@32766
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@X_GT_EQ_THAN_ZERO7
D; JGE
@X_LESS_THAN_ZERO7
0; JMP
(X_GT_EQ_THAN_ZERO7)
@R14
D=M
@SAME_SIGN7
D; JGE
@IS_TRUE_7
0; JMP
(X_LESS_THAN_ZERO7)
@R14
D=M
@SAME_SIGN7
D; JLT
@IS_FALSE_7
0; JMP
(SAME_SIGN7)
@R13
D=M
@R14
D=D-M
@IS_TRUE_7
D; JGT
@IS_FALSE_7
0; JMP
(IS_TRUE_7)
@R15
M=-1
@PUT_RESULT_IN_STACK_7
0; JMP
(IS_FALSE_7)
@R15
M=0
@PUT_RESULT_IN_STACK_7
0; JMP
(PUT_RESULT_IN_STACK_7)
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@32766
D=A
@0
A=M
M=D
@0
M=M+1
@32767
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@X_GT_EQ_THAN_ZERO8
D; JGE
@X_LESS_THAN_ZERO8
0; JMP
(X_GT_EQ_THAN_ZERO8)
@R14
D=M
@SAME_SIGN8
D; JGE
@IS_TRUE_8
0; JMP
(X_LESS_THAN_ZERO8)
@R14
D=M
@SAME_SIGN8
D; JLT
@IS_FALSE_8
0; JMP
(SAME_SIGN8)
@R13
D=M
@R14
D=D-M
@IS_TRUE_8
D; JGT
@IS_FALSE_8
0; JMP
(IS_TRUE_8)
@R15
M=-1
@PUT_RESULT_IN_STACK_8
0; JMP
(IS_FALSE_8)
@R15
M=0
@PUT_RESULT_IN_STACK_8
0; JMP
(PUT_RESULT_IN_STACK_8)
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@32766
D=A
@0
A=M
M=D
@0
M=M+1
@32766
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@X_GT_EQ_THAN_ZERO9
D; JGE
@X_LESS_THAN_ZERO9
0; JMP
(X_GT_EQ_THAN_ZERO9)
@R14
D=M
@SAME_SIGN9
D; JGE
@IS_TRUE_9
0; JMP
(X_LESS_THAN_ZERO9)
@R14
D=M
@SAME_SIGN9
D; JLT
@IS_FALSE_9
0; JMP
(SAME_SIGN9)
@R13
D=M
@R14
D=D-M
@IS_TRUE_9
D; JGT
@IS_FALSE_9
0; JMP
(IS_TRUE_9)
@R15
M=-1
@PUT_RESULT_IN_STACK_9
0; JMP
(IS_FALSE_9)
@R15
M=0
@PUT_RESULT_IN_STACK_9
0; JMP
(PUT_RESULT_IN_STACK_9)
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@57
D=A
@0
A=M
M=D
@0
M=M+1
@31
D=A
@0
A=M
M=D
@0
M=M+1
@53
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@R14
D=D+M
@R15
M=D
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@112
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@R14
D=D-M
@R15
M=D
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=-M
@R15
M=D
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@R14
D=D&M
@R15
M=D
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@82
D=A
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R14
M=D
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=M
@R14
D=D|M
@R15
M=D
@R15
D=M
@0
A=M
M=D
@0
M=M+1
@0
M=M-1
A=M
D=M
@R13
M=D
@R13
D=!M
@R15
M=D
@R15
D=M
@0
A=M
M=D
@0
M=M+1
(END)
@END
0;JMP
