import re

class Compiler():

    OPERATORS_SYMBOLS = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
    KEYWORD_CONSTANT = ['true', 'false', 'null', 'this']

    def __init__(self, tokens):
        """
        
        Args:
            tokens (list[str]): Stream of tokens.
        
        """
        self.tokens = tokens
        self.pointer = 0
        self.compiled_pg = ''


    @staticmethod
    def get_tag_and_body(s):
        """
        Returns the tag type and body as a tuple.

        .. note:: 
            The \1 in </\1> ensures that the closing tag matches the opening
            tag.
        
        Returns:
            tuple: (tag type, body)
        """
        match = re.search(r'<([^>]+)>(.+)</\1>', s)
        return (match.group(1), match.group(2).strip()) 

    @staticmethod
    def get_integerconstant_term(s):
        tag, body = Compiler.get_tag_and_body(s)
        if tag == 'integerConstant':
            return body
        return None
    
    @staticmethod
    def get_stringconstant_term(s):
        tag, body = Compiler.get_tag_and_body(s)
        if tag == 'stringConstant':
            return body
        return None
    
    @staticmethod
    def get_keywordconstant_term(s):
        tag, body = Compiler.get_tag_and_body(s)
        if tag == 'keyword' and body in Compiler.KEYWORD_CONSTANT:
            return body
        return None

    @staticmethod
    def get_identifier_term(s):
        tag, body = Compiler.get_tag_and_body(s)
        if tag == 'identifier':
            return body
        return None

    @staticmethod
    def get_operator_term(s):
        tag, body = Compiler.get_tag_and_body(s)
        if tag == 'symbol' and body in Compiler.OPERATORS_SYMBOLS:
            return body
        return None
    
    def get_token(self):
        """                
        """
        try:
            t = self.tokens[self.pointer]
            self.pointer += 1
            return t
        except IndexError:
            return None
        
    def get_verified_symbol(self, expected):
        """
        Returns the expected symbol within tags. Raises an exception if symbol
        is not the expected.
        """

        _, body = Compiler.get_tag_and_body(self.get_token())
        if body != expected:
            raise ValueError(
                f'Token {body} does not much expected symbol of {expected}')
        return f'<symbol> {body} </symbol>\n'

    def compile_varname(self):

        t = self.get_token()
        varname = self.get_identifier_term(t)
        if varname is not None:
            return f'<identifier> {varname} </identifier>\n'
        else:
            raise Exception(
                f'Compilation failed. Expected a varname. Received {varname}')

    def compile_term(self):

        def _wrap(inner):
            return f'<term>\n{inner}</term>\n'
        
        t = self.get_token()
       
        # term is integerConstant
        integer_constant = self.get_integerconstant_term(t)
        if integer_constant is not None:
            return _wrap(
                f'<integerConstant> {integer_constant} </integerConstant>\n')
        
        # term is stringConstant
        string_constant = self.get_stringconstant_term(t)
        if string_constant is not None:
            return _wrap(
                f'<stringConstant> {string_constant} </stringConstant>\n')

        # term is keywordConstant
        keyword_constant = self.get_keywordconstant_term(t)
        if keyword_constant is not None:
            return _wrap('<keyword> {keyword_constant} </keyword>\n')

        # term is varName        
        varname = self.get_identifier_term(t)
        if varname is not None:
            return _wrap(f'<identifier> {varname} </identifier>\n')
        
        raise Exception(f'Compiling `term` failed. Source code {t}')


    def compile_expression(self):
        
        # Get first term
        term = self.compile_term()

        # If next token is not an operator expression is finished
        next_token = self.get_token()
        op = self.get_operator_term(next_token)
        if op is None:
            self.pointer -= 1
            inner = term
        else:
            inner = term + f'<symbol> {op} </symbol>\n' + self.compile_term()

        return f'<expression>\n{inner}</expression>\n'

    def compile_let_stm(self):

        s = (
            f'<letStatement>\n'
            f'<keyword> let </keyword>\n'
            f'{self.compile_varname()}'
            f'{self.get_verified_symbol("=")}'

            f'{self.compile_expression()}'
            f'{self.get_verified_symbol(";")}'
            f'</letStatement>\n'
        )
        return s

    def compile(self):

        t = self.get_token()
        while t is not None:

            tag, body = self.get_tag_and_body(t)

            if body == 'let':
                out = self.compile_let_stm()
            else:
                raise Exception

            self.compiled_pg += out
            t = self.get_token()

