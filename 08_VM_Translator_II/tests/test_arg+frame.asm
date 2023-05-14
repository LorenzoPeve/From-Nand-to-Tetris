// INITIALIZE STACK
@22
D=A
@8
M=D

@23
D=A
@9
M=D

@77
D=A
@10
M=D

@78
D=A
@11
M=D

// SET SP
@12
D=A
@0
M=D

// Set LCL, ARG, THIS THAT
@20
D=A
@1
M=D

@25
D=A
@2
M=D

@30
D=A
@3
M=D

@40
D=A
@4
M=D


// SAVE FRAME
@1
D=M
@0
A=M
M=D
@0
M=M+1
@2
D=M
@0
A=M
M=D
@0
M=M+1
@3
D=M
@0
A=M
M=D
@0
M=M+1
@4
D=M
@0
A=M
M=D
@0
M=M+1

// REPOSITION ARG

@0
D=M
@2
D=D-A
@5
D=D-A
@2
M=D

@0
D=M
@1
M=D
(END)
@END
0;JMP




