class MemorySegment():


    SEGMENTS = {
        'local':1,
        'argument':2,
        'this':3,
        'that':4,
    }



    def __init__(self, line: str):
        self.op, self.segment, self.i = line.split()


    def _push_constant(self) -> str:
        """Supplies the specified constant to the stack."""
        s = (
            # Set D register to constant
            f'@{self.i}\n'
            f'D=A\n'

            # *SP=i by going to address stored in RAM[0
            f'@0\n'
            f'A=M\n'
            f'M=D\n'
            
            # SP++
            f'@0\n'
            f'M=M+1\n'
        )
        return s


    def _basic_push_operation(self):
        """Push the value of segment[index] onto the stack."""
        segment_pointer = self.SEGMENTS[self.segment] + self.i # address
        s = (
            # D=i
            f'@{self.i}\n'
            f'D=A\n'

            # (addr = SegmentPointer+i) and (D=*addr)
            f'@{segment_pointer}\n'
            f'A=D+M\n'
            f'D=M'

            f'@0\n'     # *SP=D=*addr
            f'A=M\n'
            f'M=D\n'            
            
            f'@0\n'     # SP++
            f'M=M+1\n'
        )
        return s
    
    def _basic_pop_operation(self):
        """Pops the top stack value and stores it in segment[index]"""

        # Note

        segment_pointer = self.SEGMENTS[self.segment] + self.i # address
        s = (
            
            # 1. Get the value from the stack to a register
            
            # SP--
            f'@0\n' 
            f'M=M-1\n'

            # @R13=*SP
            f'A=M\n'
            f'D=M\n'
            f'@R13\n'
            f'M=D\n'

            # D=i
            f'@{self.i}\n'
            f'D=A\n'

            # (addr = SegmentPointer+i) and (D=*addr)
            f'@{segment_pointer}\n'
            f'A=D+M\n'










        )
        return s


    def translate_memory(self):

        if self.segment == 'constant':
            return self._push_constant().split('\n')
        
        elif self.segment in ['local', 'argument', 'this', 'that']:
            if self.op == 'push':
                return self._basic_push_operation().split('\n')
            elif self.op == 'pop':
                return self._basic_pop_operation().split('\n')
            else:
                raise ValueError(
                    f"{self.op} {self.segment} {self.i} couldn't be mapped."
                    )






