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
IDENTIFIER_REGEX = re.compile(r'[A-Za-z_][a-zA-Z0-9_]*$')

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

def _split_at_symbols(s):
    """
    Returns a list with the original string splitted at symbols locations.    

    If there are no symbols, it returns a single element list with original
    string.

    Returns:
        list: List of strings.
    """

    loc = None
    for index, character in enumerate(s):
        if character in SYMBOLS:
            loc = index
            break

    if loc is None:
        return [s]

    return [s[0:loc]] + [s[loc]] + _split_at_symbols(s[loc+1:])

def _get_quotation_marks_locs(s):
    """
    Returns locations of `"`. Raises an exception if a string is never closed.    
    """
    locs = []
    for i, char in enumerate(s):
        if char == '"':
            locs.append(i)

    if len(locs) % 2 != 0:
        raise ValueError(
            f'String constant is malformed. Number of " is {len(locs)}')
    return locs

def _split_at_non_string_spaces(s):
    """
    Returns a list of strings by splitting at non-string spaces.

    'if "hello world"' > ['if', '"hello world"']    
    """
    locs = _get_quotation_marks_locs(s)
    if len(locs) == 0:
        return s.split(' ')

    return (
        s[:locs[0]].split(' ') + 
        [s[locs[0]:locs[1]+1]] + # This is the string constant
        _split_at_non_string_spaces(s[locs[1]+1:])
    )

def parse(s):
    """
    Parses a line of Jack code into a list of tokens splitting at symbols and
    at empty spaces.

    Args:
        s (str): Line of Jack code.

    Returns
        list[str]: List of tokens after splitting at symbols and at empty
        spaces and after removing empty strings.
    """
    token_list = _split_at_symbols(s)
    
    # Remove empty strings and strip
    token_list_pro = []
    for i in token_list:
        if len(s) > 0:
            token_list_pro.append(i.strip())

    # Split list at spaces. Watchout for string constants
    token_list_splitted = []
    for characters in token_list_pro:
        token_list_splitted.extend(
            _split_at_non_string_spaces(characters))

    out = [s for s in token_list_splitted if len(s) > 0]
    return out


def analyze(line):
    """
    
    Args:
        line (str): A line from a Jack Program

    Returns:
        (str): Tokens with tags.

    Split line at spaces and symbols    
    """    
    processed_line = parse(line)
    output = ""
    for s in processed_line:
        
        if is_keyword(s):
            output += f'<keyword> {s} </keyword>\n'
        elif is_symbol(s):

            # (<), (>), (&) are outputted as &lt &gt, and &amp
            if s == '<':
                s = '&lt;'
            elif s == '>':
                s = '&gt;'
            elif s == '&':
                s = '&amp;'

            output += f'<symbol> {s} </symbol>\n'
        elif is_integer(s):
            output += f'<intConst> {s} </intConst>\n'
        elif is_string(s):
            # String constants are outputted without the double-quotes
            output += f'<stringConst> {s[1:-1]} </stringConst>\n'
        elif is_identifier(s):
            output += f'<identifier> {s} </identifier>\n'
        else:
            raise ValueError(f'Character(s) [{s}] could not be mapped.')
    
    return output