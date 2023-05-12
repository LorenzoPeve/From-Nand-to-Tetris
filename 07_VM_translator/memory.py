class MemorySegment():


    SEGMENTS = {
        'local':1,
        'argument':2,
        'this':3,
        'that':4,
    }


    def __init__(self, line: str, fname: str):
        self.op, self.segment, self.i = line.split()
        self.i = int(self.i)
        self.fname = fname

    def _increase_stack_pointer(self):
        return '@0\nM=M+1\n'

    def _decrease_stack_pointer(self):
        return '@0\nM=M-1\n'

    def _put_D_at_pointer_address(self):
        """Sets the next available pointer location to the D-register value."""
        return '@0\nA=M\nM=D\n'    

    def _put_target_push_value_into_D(self):
        """
        Puts the value of segment[index] into D-register.
        addr= SegmentPointer+i (unless temp). Then D=*addr.
        """
        if self.segment not in ['temp', 'pointer']:
            segment_pointer = self.SEGMENTS[self.segment]
            return (
                f'@{self.i}\n'
                f'D=A\n'
                f'@{segment_pointer}\n'
                f'A=D+M\n'
                f'D=M\n'
            )
        elif self.segment == 'temp':
            return (
                f'@{5 + self.i}\n'
                f'D=M\n'
            )
        elif self.segment == 'pointer' and self.i == 0:
            return '@3\nD=M\n'
        elif self.segment == 'pointer' and self.i == 1:
            return '@4\nD=M\n'

    def _put_target_address_into_R13(self):
        if self.segment not in ['temp', 'pointer']:
            segment_pointer = self.SEGMENTS[self.segment]
            s = (
                f'@{self.i}\n'
                f'D=A\n'
                f'@{segment_pointer}\n'
                f'D=D+M\n'
            )
        elif self.segment == 'temp':
            s = (
                f'@{5 + self.i}\n'
                f'D=A\n'
            )
        elif self.segment == 'pointer' and self.i == 0:
            s = '@3\nD=A\n'
        elif self.segment == 'pointer' and self.i == 1:
            s ='@4\nD=A\n'

        return s + '@R13\nM=D\n'
        
    def _push_constant(self) -> str:
        """Supplies the specified constant to the stack."""
        s = (
            # Set D register to constant
            f'@{self.i}\n'
            f'D=A\n'
            f'{self._put_D_at_pointer_address()}'            
            f'{self._increase_stack_pointer()}'
        )

        return s
    
    def _basic_push_operation(self):
        """Push the value of segment[index] onto the stack."""

        s = (
            f'{self._put_target_push_value_into_D()}'
            f'{self._put_D_at_pointer_address()}'            
            f'{self._increase_stack_pointer()}'
        )
        return s
    
    def _basic_pop_operation(self):
        """Pops the top stack value and stores it in segment[index]"""
        s = (
            f'{self._put_target_address_into_R13()}'
            f'{self._decrease_stack_pointer()}'

            # Get value from stack
            f'A=M\n'
            f'D=M\n'

            # Place value from stack at the correct address
            f'@R13\n'
            f'A=M\n'
            f'M=D\n'
        )
        return s


    def _static_pop_operation(self):
        "Pops value from stack and stores it into global space"
        return (
            f'{self._decrease_stack_pointer()}'
            f'@0\n'
            f'A=M\n'
            f'D=M\n'
            f'@{self.fname}.{self.i}\n' # Foo.vm pop static 5 Foo.5
            f'M=D\n'
        )

    def _static_push_operation(self):
        "Pushes value from global space into stack"
        return (         
            f'@{self.fname}.{self.i}\n' # Foo.vm push static 5 Foo.5
            f'D=M\n'
            f'@0\n'
            f'A=M\n'
            f'M=D\n'
            f'{self._increase_stack_pointer()}'
        )

    def translate_memory(self):
        
        if self.segment == 'constant':
            return self._push_constant().split('\n')
        
        if self.segment == 'static':
            if self.op == 'push':
                return self._static_push_operation().split('\n')
            else:
                return self._static_pop_operation().split('\n')
                    
        # Check that temp is between 5-12
        if self.segment == 'temp':
            assert self.i >= 0 and self.i <=7, f'Temp only goes 5-12'

        if self.op == 'push':
            return self._basic_push_operation().split('\n')
        elif self.op == 'pop':
            return self._basic_pop_operation().split('\n')           
        else:
            raise ValueError(
                    f"{self.op} {self.segment} {self.i} couldn't be mapped."
                    )