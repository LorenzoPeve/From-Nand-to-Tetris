"""Repetition in support of readibility and expresiveness"""

OPS = {

    'add':(
        f'@R13\n'
        f'D=M\n'
        f'@R14\n'
        f'D=D+M\n'
        ),

    'sub':(
        f'@R13\n'
        f'D=M\n'
        f'@R14\n'
        f'D=D-M\n'
        ),

    'neg': (
        f'@R13\n'
        f'D=-M\n'
        ),
    'and': (
        f'@R13\n'
        f'D=M\n'
        f'@R14\n'
        f'D=D&M\n'
        ),
    'or': (
        f'@R13\n'
        f'D=M\n'
        f'@R14\n'
        f'D=D|M\n'
        ),
    'not': (
        f'@R13\n'
        f'D=!M\n'
        ),
}

class Arithmetic:

    """
    Note: Design decision is to store operands in registers R13 and R14 and
    result computation in R15.
    
    """
    
    allowed = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']    
    arg1_register = 'R13'
    arg2_register = 'R14'
    counter = 1

    def __init__(self, operation: str) -> None:
        if operation not in self.allowed:
            raise ValueError(f'Operation not available in stack arithmetic')
        self.op = operation
        self.ins = ''

    @staticmethod
    def _retrieve_operand_from_stack(register: str) -> str:
        """
        Gets the element referenced by the current stack pointer and stores it
        at the input register.

        Recall stack pointer refers to next available location.

        Pseudo-code:    num=*SP--, add=register, *add=num
        """        
        return (
            f'@0\n'
            f'M=M-1\n'
            f'A=M\n'
            f'D=M\n'
            f'@{register}\n'
            f'M=D\n'
        )

    def _retrieve_operands(self) -> str:
        """
        Retrieves operand(s) needed for computation by storing them in 
        predefined registers.
        """        
        if self.op in  ['neg', 'not']:            
            self.ins += self._retrieve_operand_from_stack(self.arg1_register)
        else:
            # Put (y) in R14 and (x) in R13
            self.ins += self._retrieve_operand_from_stack(self.arg2_register)
            self.ins += self._retrieve_operand_from_stack(self.arg1_register)
        
    def _perform_operation(self):
        """
        Computes an operation using R13 and R14 as operands, storing the value
        in the D-register and then putting it in R15.
        """
        if self.op not in ['eq', 'gt', 'lt']:
            self.ins += OPS[self.op] + '@R15\nM=D\n'
        else:
            func = getattr(self.__class__, self.op)
            self.ins += func(self)

    def _put_back_in_stack(self):
        """
        Gets the computation result from R15 and stores it at the stack
        pointer.
        """
        
        s = (
            f'@R15\n'       # Go to register 15
            f'D=M\n'        # Read the contents @R15
            f'@0\n'         
            f'A=M\n'        # Go to the next available location
            f'M=D\n'        # Store D
            f'@0\n'         # Increment pointer by one
            f'M=M+1\n'
        )        
        
        self.ins += s

    def translate_arithmetic(self) -> list[str]:

        self._retrieve_operands() # Put operand(s) in registers R13 and R14
        self._perform_operation() # Performs the operation and stores it in R15
        self._put_back_in_stack() # Puts the result in R15 back in the stack
        return self.ins.split('\n')

    @classmethod
    def increase_counter(cls):
        cls.counter += 1


    def eq(self):
        s = (
            f'@R13\n'
            f'D=M\n'
            f'@R14\n'
            f'D=D-M\n'
            f'@IS_EQUAL_{self.counter}\n'
            f'D; JEQ\n'
            f'@R15\n'
            f'M=0\n'
            f'@PUT_RESULT_IN_STACK_{self.counter}\n'
            f'0; JMP\n'
            f'(IS_EQUAL_{self.counter})\n'
            f'@R15\n'
            f'M=-1\n'
            f'(PUT_RESULT_IN_STACK_{self.counter})\n'
        )
        self.increase_counter()
        return s

    def lt(self):

        s = (
            f'@R13\n'
            f'D=M\n'

            f'@X_GT_EQ_THAN_ZERO{self.counter}\n'
            f'D; JGE\n'

            f'@X_LESS_THAN_ZERO{self.counter}\n'
            f'0; JMP\n'

            # x >= 0
            f'(X_GT_EQ_THAN_ZERO{self.counter})\n'
            f'@R14\n'
            f'D=M\n'
            f'@SAME_SIGN{self.counter}\n'
            f'D; JGE\n'

            # x >= 0 and y < 0. Thus, False
            f'@IS_FALSE_{self.counter}\n'
            f'0; JMP\n'

            # x < 0
            f'(X_LESS_THAN_ZERO{self.counter})\n'
            f'@R14\n'
            f'D=M\n'
            f'@SAME_SIGN{self.counter}\n'
            f'D; JLT\n'

            # x < 0 and y >= 0. Thus, True
            f'@IS_TRUE_{self.counter}\n'
            f'0; JMP\n'

            # If (x>=0 and y>=0) or (x<0 and y<0)
            f'(SAME_SIGN{self.counter})\n'
            f'@R13\n' 
            f'D=M\n'  # D = x
            f'@R14\n'
            f'D=D-M\n' # D = x-y. If D <0, x is less than y
            f'@IS_TRUE_{self.counter}\n'
            f'D; JLT\n'
            f'@IS_FALSE_{self.counter}\n'
            f'0; JMP\n'            

            f'(IS_TRUE_{self.counter})\n'
            f'@R15\n'
            f'M=-1\n'
            f'@PUT_RESULT_IN_STACK_{self.counter}\n'
            f'0; JMP\n'

            f'(IS_FALSE_{self.counter})\n'
            f'@R15\n'
            f'M=0\n'
            f'@PUT_RESULT_IN_STACK_{self.counter}\n'
            f'0; JMP\n'

            f'(PUT_RESULT_IN_STACK_{self.counter})\n'
        )

        self.increase_counter()
        return s
    
    def gt(self):
        s = (
            f'@R13\n'
            f'D=M\n'

            f'@X_GT_EQ_THAN_ZERO{self.counter}\n'
            f'D; JGE\n'

            f'@X_LESS_THAN_ZERO{self.counter}\n'
            f'0; JMP\n'

            # x >= 0
            f'(X_GT_EQ_THAN_ZERO{self.counter})\n'
            f'@R14\n'
            f'D=M\n'
            f'@SAME_SIGN{self.counter}\n'
            f'D; JGE\n'

            # x >= 0 and y < 0. Thus, False
            f'@IS_TRUE_{self.counter}\n'
            f'0; JMP\n'

            # x < 0
            f'(X_LESS_THAN_ZERO{self.counter})\n'
            f'@R14\n'
            f'D=M\n'
            f'@SAME_SIGN{self.counter}\n'
            f'D; JLT\n'

            # x < 0 and y >= 0. Thus, True
            f'@IS_FALSE_{self.counter}\n'
            f'0; JMP\n'

            # If (x>=0 and y>=0) or (x<0 and y<0)
            f'(SAME_SIGN{self.counter})\n'
            f'@R13\n' 
            f'D=M\n'  # D = x
            f'@R14\n'
            f'D=D-M\n' # D = x-y. If D <0, x is less than y
            f'@IS_TRUE_{self.counter}\n'
            f'D; JGT\n'
            f'@IS_FALSE_{self.counter}\n'
            f'0; JMP\n'            

            f'(IS_TRUE_{self.counter})\n'
            f'@R15\n'
            f'M=-1\n'
            f'@PUT_RESULT_IN_STACK_{self.counter}\n'
            f'0; JMP\n'

            f'(IS_FALSE_{self.counter})\n'
            f'@R15\n'
            f'M=0\n'
            f'@PUT_RESULT_IN_STACK_{self.counter}\n'
            f'0; JMP\n'

            f'(PUT_RESULT_IN_STACK_{self.counter})\n'
        )
                        
        self.increase_counter()
        return s




if __name__ == '__main__':
    c = Arithmetic('add')
    print(c._retrieve_operands())


  