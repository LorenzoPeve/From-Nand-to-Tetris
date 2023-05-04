class MemorySegment():


    SP=0
    LCL=1
    ARG=2
    THIS=3
    THAT=4


    def __init__(self, line: str):
        self.op, self.segment, self.i = line.split()



    def _constant(self) -> str:

        return (
            f'@{self.i}\n' # Set D register to constant
            f'D=A\n'

            f'@0\n'     # *SP=i
            f'A=M\n'
            f'M=D\n'
            
            f'@0\n'     # SP++
            f'M=M+1\n'
        )


    def translate_memory(self):
        if self.segment == 'constant':
            return self._constant().split('\n')




