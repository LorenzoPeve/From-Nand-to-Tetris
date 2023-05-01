class Arithmetic:

    # Pops the argument(s) from the stack
    # Computes f on the arguments
    # Pushed the result onto the stack
    """
    note

    arg1 is stored in R13 and arg2 is stored in R14
    
    """
    

    allowed = [
        'add', 'sub', 'neg', 'eq', 'gt',
        'lt', 'and', 'or', 'not'
    ]
    
    arg1_register = 'R13'
    arg2_register = 'R14'

    def __init__(self, operation: str) -> None:
        if operation not in self.allowed:
            raise ValueError(f'Operation not available in stack arithmetic')
        self.op = operation

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


    def _retrieve_operands(self) -> list[str]:
        
        ins = self._retrieve_operand_from_stack(self.arg1_register)
        
        # Unless operation is `neg` return next operand
        if self.op != 'neg':
            ins += self._retrieve_operand_from_stack(self.arg2_register)
        
    def _perform_operation(self):
        pass

    def _put_back_in_stack(self):
        pass

if __name__ == '__main__':
    c = Arithmetic('add')
  