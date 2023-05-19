class Function:

    counter = 1 # simple way of having unique labels

    def __init__(self, command: str) -> None:
        self.command = command

    def _increase_stack_pointer(self):
        return '@0\nM=M+1\n'

    def _decrease_stack_pointer(self):
        return '@0\nM=M-1\n'

    def _function_f_k(self):
        _, fname, n_vars = self.command.split(' ')
        
        s = f'({fname})\n'

        for i in range(int(n_vars)):
            s+= f'// Initializing local variable {i+1}/{n_vars}\n'
            s+= f'@0\nA=M\nM=0\n'
            s+= self._increase_stack_pointer()

        return s
    
    def _reposition_arg(self, n):
        """Reposition ARG=SP-n-5"""
        return (
            # Get SP
            f'@0\n'
            f'D=M\n'

            # D=SP-n
            f'@{n}\n'
            f'D=D-A\n'

            # D=D-5 (i.e D = SP-n-5)
            f'@5\n'
            f'D=D-A\n'
            
            # Store D @ RAM[2]
            f'@2\n'
            f'M=D\n'
        )
    
    def _push_pointer_to_stack(self, ram):
        """Pushes a pointer store at RAM[ram] to the stack"""
        return (
            f'@{ram}\n'
            f'D=M\n'
            f'@0\n'
            f'A=M\n'
            f'M=D\n'
            f'{self._increase_stack_pointer()}'
            )

    def _save_frame_of_caller(self):
        return (
            f'{self._push_pointer_to_stack(1)}'  # Saves LCL of the caller
            f'{self._push_pointer_to_stack(2)}'  # Saves ARG of the caller
            f'{self._push_pointer_to_stack(3)}'  # Saves THIS of the caller
            f'{self._push_pointer_to_stack(4)}'  # Saves THAT of the caller
        )   
    
    def _call_f_n(self): # -> str
        _, fname, n_args = self.command.split(' ')
        
        label = f'{fname}$ret.{self.counter}'

        # Save return address
        s0 = (
            f'@{label}\n' # It will change to a number
            f'D=A\n'
            f'@0\n'
            f'A=M\n'
            f'M=D\n'
            f'{self._increase_stack_pointer()}'
        )
        s1 = self._save_frame_of_caller()       # Save frame
        s2 = self._reposition_arg(int(n_args))  # ARG = SP-n-5
        s3 ='@0\nD=M\n@1\nM=D\n'                # LCL = SP
        s4 = f'@{fname}\n0; JMP\n'   # goto function        
        s5 = f'({label})\n'

        Function.counter +=1
        return s0 + s1 + s2 + s3 + s4 + s5

    def _point_to_frame_minus_n(self, n):
        """Sets D-register to *(FRAME-n)."""
        return (
            f'@{n}\n'
            f'D=A\n'
            f'@13\n'
            f'A=M-D\n'
            f'D=M\n'
        )

    def _return_f(self): # -> str
        s = (
            
            # RAM[13] = LCL = RAM[1]. Use RAM[13] as temp variable
            f'@1\n'
            f'D=M\n'
            f'@13\n'
            f'M=D\n'

            # RAM[14] = RET = return address
            f'{self._point_to_frame_minus_n(5)}'
            f'@14\n'
            f'M=D\n'

            # Push value from stack to (i.e., *ARG = pop())
            f'@0\n'
            f'M=M-1\n'
            f'A=M\n'
            f'D=M\n'
            f'@2\n'
            f'A=M\n'
            f'M=D\n'

            # SP = ARG+1
            f'D=A\n'
            f'@0\n'
            f'M=D\n'
            f'M=M+1\n'

            # Restore THAT of the caller
            f'{self._point_to_frame_minus_n(1)}'
            f'@4\n'
            f'M=D\n'

            # Restore THIS of the caller
            f'{self._point_to_frame_minus_n(2)}'
            f'@3\n'
            f'M=D\n'

            # Restore ARG of the caller
            f'{self._point_to_frame_minus_n(3)}'
            f'@2\n'
            f'M=D\n'

            # Restore LCL of the caller
            f'{self._point_to_frame_minus_n(4)}'
            f'@1\n'
            f'M=D\n'

            # JUMP
            f'@14\n'
            f'A=M\n'
            f'0;JMP\n'
        )

        return s

    def translate(self):

        if self.command.startswith('function'):
            return self._function_f_k().split('\n')

        elif self.command.startswith('call'):
            return self._call_f_n().split('\n')
        
        elif self.command.startswith('return'):
            return self._return_f().split('\n')
        
        else:
            raise Exception(f'Line couldnt be parsed {self.command}')
