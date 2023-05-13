class Branch:

    def __init__(self, command: str) -> None:
        self.command = command

    def translate_branch(self):        
        
        if self.command.startswith('label'):
            s = self.command.replace('label ', "")
            return [f'({s})']
        
        elif self.command.startswith('goto'):
            s = self.command.replace('goto ', "")
            s = (
                f'@{s}\n'
                f'0; JMP\n'
            )
            return s.split('\n')[:-1]
        
        elif self.command.startswith('if-goto'):
            label = self.command.replace('if-goto ', "")
            s = (
                # Pop value of stack and put it D register
                f'@0\n'
                f'M=M-1\n'
                f'A=M\n'
                f'D=M\n'

                # Evaluate condition. If D !=0, then JUMP
                f'@{label}\n'
                f'D;JNE\n'
            )
            return s.split('\n')[:-1]