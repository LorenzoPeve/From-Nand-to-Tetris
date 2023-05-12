# Note: Methods with type hint are commented out because grader uses older
# Python version

class Reader():

    def __init__(self, fpath) -> None:
        self.fpath = fpath

    def remove_whitespace(self, data):  # data: list[str]) -> list:
        return [line.strip() for line in data]

    def remove_empty_lines(self, data):  # data: list[str]) -> list:
        return [line for line in data if len(line) > 1]

    def remove_comment_lines(self, data):  # data: list[str]) -> list:
        return [line for line in data if not line.startswith('//')]

    def remove_inline_comments(self, data):  # data: list[str]) -> None:
        for i, line in enumerate(data):
            if '//' in line:
                idx = line.find('//')
                line = line[:idx]
                data[i] = line.strip()

    def remove_whitespace_within(self, data):  # data: list[str]) -> list:
        return [" ".join(s.strip().split()) for s in data]

    def read(self): # -> list:
        with open(self.fpath) as f:
            data = f.readlines()

        data = self.remove_whitespace(data)
        data = self.remove_empty_lines(data)
        data = self.remove_comment_lines(data)
        self.remove_inline_comments(data)
        data = self.remove_whitespace_within(data)
        return data
