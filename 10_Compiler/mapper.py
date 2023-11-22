import re

KEYWORDS = [
    'class', 'constructor', 'function', 'method', 'field', 'static', 'var',
    'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let',
    'do', 'if', 'else', 'while', 'return'
]

SYMBOLS = [
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|',
    '<', '>', '=', '~',
]

INTEGER_REGEX = re.compile(r'[0-9]+$')
STRING_REGEX = re.compile(r'"[^"]+"$')
IDENTIFIER_REGEX = re.compile(r'[A-Za-z_][a-zA-Z0-9_]+$')

def is_keyword(token):
    return token in KEYWORDS

def is_symbol(token):
    return token in SYMBOLS

def is_integer(token):
    """Returns True if token is a decimal in the range 0 to 32767."""
    return bool(INTEGER_REGEX.match(token))

def is_string(token):
    """    
    Returns True is token is a string.
    
    Note: JACK grammar says a sequence of UNICODE characters not including
    double quote or new line. I tried both ("") and ("\n") and the JACK
    compiler worked no problem.
    """
    return bool(STRING_REGEX.match(token))

def is_identifier(token):
    """
    Returns True is token is an identifier.
    
    In JACK grammar an identifier is a sequence of letters, digits, and
    underscore not starting with a digit.    
    """
    return bool(IDENTIFIER_REGEX.match(token))

def split_at_symbols(s):
    """
    Returns a list with the original string splitted at symbols locations.    

    If there are no symbols, it returns a single element list with original
    string.
    """

    loc = None
    for index, character in enumerate(s):
        if character in SYMBOLS:
            loc = index
            break

    if loc is None:
        return [s]

    return [s[0:loc]] + [s[loc]] + split_at_symbols(s[loc+1:])

def analyze(line):
    """
    
    Args:
        (line): A line from a Jack Program

    Split line at spaces and symbols   
    
    """
    
    splitted_line = split_at_symbols(line)
    splitted_line = [s for s in splitted_line if len(s)>0]

