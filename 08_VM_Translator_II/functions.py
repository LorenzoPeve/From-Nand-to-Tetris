class Function:

    def __init__(self, command: str) -> None:
        self.command = command

    def _function_f_k(self):
        pass

    def translate_branch(self):

        if self.command.startswith('function'):
            pass

        elif self.command.startswith('call'):
            pass

        else:
            raise Exception(f'Line couldnt be parsed {self.command}')
