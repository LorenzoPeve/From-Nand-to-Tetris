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

    @staticmethod
    def _remove_api_comments(data):
        
        api_com_start = []
        api_com_end = []
        for idx, line in enumerate(data):
            if '/**' in line:
                api_com_start.append(idx)
            if '*/' in line:
                api_com_end.append(idx)

        if len(api_com_start) != len(api_com_end):
            raise ValueError('API comments malformed.')
        
        if len(api_com_start) == 0:
            return data
        else:
            data_no_api = data[:api_com_start[0]] + data[api_com_end[0]+1:]
            return _Reader._remove_api_comments(data_no_api)

    def read(self):
        self.data = self._remove_whitespace()
        self.data = self._remove_empty_lines()
        self.data = self._remove_comment_lines()
        self._remove_inline_comments()
        self.data = _Reader._remove_api_comments(self.data)
        return self.data

class Tokenizer():
    """
    Ignores all comments and white space in the input stream, and serializes it
    into Jack-language tokens according to Jack grammar.
    """

    def __init__(self, fpath=None, stream=None):
        """Initializes a tokenizer by passing a filepath or the data itself."""
        if fpath is not None:
            self.fpath = fpath
            path = Path(fpath)
            self.filename = path.stem

            with open(self.fpath) as f:
                data = f.readlines()
                self.stream = _Reader(data).read()

        if stream is not None:
            self.stream = stream
 
    def tokenize(self, headers='tokens'):
        """
        Args:
            headers (str): XML-headers. Required when tokenizing non-classes
                Jack programs for correct XML rendering.
        """
        if len(headers) > 0:
            tokens = f'<{headers}>\n'
        else:
            tokens = ''

        for line in self.stream:
            tokens += mapper.analyze(line)
        
        if len(headers) > 0:
            return tokens + f'</{headers}>\n'
        else:
            return tokens