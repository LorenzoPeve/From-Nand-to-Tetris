import os
from pathlib import Path

import mapper

class _Reader():

    def __init__(self, data):
        self.data = data

    def _remove_whitespace(self):
        return [line.strip() for line in self.data]

    def _remove_empty_lines(self):
        return [line for line in self.data if len(line) >= 1]

    def _remove_comment_lines(self):
        return [line for line in self.data if not line.startswith('//')]

    def _remove_inline_comments(self):
        for i, line in enumerate(self.data):
            if '//' in line:
                idx = line.find('//')
                line = line[:idx]
                self.data[i] = line.strip()

    def read(self):
        self.data = self._remove_whitespace()
        self.data = self._remove_empty_lines()
        self.data = self._remove_comment_lines()
        self._remove_inline_comments()
        return self.data

class Tokenizer():
    """
    Ignores all comments and white space in the input stream, and serializes it
    into Jack-language tokens according to Jack grammar.
    """

    def __init__(self, fpath):
        
        self.fpath = fpath
        path = Path(fpath)
        self.filename = path.stem

        with open(self.fpath) as f:
            data = f.readlines()
            self.stream = _Reader(data).read()
 
    def tokenize(self):
        """"""
        tokens = ""
        for line in self.stream:
            tokens += mapper.analyze(line)
        
        return tokens