class MemorySegment():


    SEGMENTS = {
        'local':1,
        'argument':2,
        'this':3,
        'that':4,
    }
    counter = 1

    def __init__(self, line: str):
        self.op, self.segment, self.i = line.split()
        self.i = int(self.i)

    def _increase_stack_pointer(self):
        return '@0\nM=M+1\n'

    def _decrease_stack_pointer(self):
        return '@0\nM=M-1\n'

    def _put_D_at_pointer_address(self):
        """Sets the next available pointer location to the D-register value."""
        return '@0\nA=M\nM=D\n'    

    def _put_pushed_value_into_D(self):
        """
        Puts the value of segment[index] into D-register.
        addr= SegmentPointer+i (unless temp). Then D=*addr.
        """
        if self.segment != 'temp':
            segment_pointer = self.SEGMENTS[self.segment]
            return (
                f'@{self.i}\n'
                f'D=A\n'
                f'@{segment_pointer}\n'
                f'A=D+M\n'
                f'D=M\n'
            )
        else:
            return (
                f'@{5 + self.i}\n'
                f'D=M\n'
            )
        
    def _put_target_address_into_R13(self):
        """
        Puts the addr= SegmentPointer+i into the R13 register.
        If SegmentPointer is not initialized, address points to its RAM 
        location.
        """
        if self.segment != 'temp':
            segment_pointer = self.SEGMENTS[self.segment]
            s = (
                # Addresses case when pointer is not initialized
                f'@{segment_pointer}\n'
                f'D=M\n'
                f'@HAS_BASE_ADDRESS{self.counter}\n'
                f'D; JGT\n'
      
                
                f'@{segment_pointer}\n'
                f'D=A;\n'
                f'@PUT_RESULT_IN_R13_{self.counter}\n'
                f'0; JMP\n'


                f'(HAS_BASE_ADDRESS{self.counter})\n'
                f'@{self.i}\n'
                f'D=A\n'
                f'@{segment_pointer}\n'
                f'D=D+M\n'

                f'(PUT_RESULT_IN_R13_{self.counter})\n'

            )
        else:
            s = (
                f'@{5 + self.i}\n'
                f'D=A\n'
            )
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
            f'{self._put_pushed_value_into_D()}'
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


    def translate_memory(self):

        self.__class__.counter += 1

        # pointer implementation for W7
        if self.segment == 'pointer':
            if self.i not in [0, 1]:
                raise ValueError(f'pointer i is {self.i}. Must be 0 or 1.')
            if self.i == 0:
                self.segment = 'this'
            else:
                self.segment = 'that'

        if self.segment == 'constant':
            return self._push_constant().split('\n')
        
        elif self.segment in ['local', 'argument', 'this', 'that', 'temp']:
            
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
        else:
            raise ValueError(
                    f"{self.op} {self.segment} {self.i} couldn't be mapped."
                    )





