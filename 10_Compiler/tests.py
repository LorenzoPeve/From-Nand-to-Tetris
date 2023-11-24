import os

import mapper
from tokenizer import Tokenizer, _Reader

def _get_testfile(f: str) -> str:
    return os.path.join(
        os.path.dirname(__file__), 'tests', f)

def test_reader():
    finput = _get_testfile('SquareGame.jack')

    with open(finput) as f:
        data = f.readlines()

    t = _Reader(data)
    t.data = t._remove_whitespace()
    t.data = t._remove_empty_lines()
    t.data = t._remove_comment_lines()
    t._remove_inline_comments()
    t.data = (t._remove_api_comments(t.data))

    for i in t.data:
        if '/**' in i:
            raise ValueError

def test_tokenizer_init():
    f_input = _get_testfile('Prog.jack')
    t = Tokenizer(f_input)
    assert len(t.stream) == 3

def test_keyword():    
    assert mapper.is_keyword('class') == True
    assert mapper.is_keyword('my_class') == False
    assert mapper.is_keyword('return') == True
    assert mapper.is_keyword('return ') == False

def test_symbol():
    assert mapper.is_symbol('+') == True
    assert mapper.is_symbol('+ ') == False
    assert mapper.is_symbol('?') == False
    assert mapper.is_symbol('/') == True

def test_integer():
    assert mapper.is_integer('1') == True
    assert mapper.is_integer('12345') == True
    assert mapper.is_integer('123456') == True
    assert mapper.is_integer('123456w') == False
    assert mapper.is_integer(' 123456') == False
    assert mapper.is_integer('1 23456') == False
    assert mapper.is_integer('12 ') == False

def test_string():
    assert mapper.is_string('"This is a string"') == True
    assert mapper.is_string('"This is a 12345 string"') == True
    assert mapper.is_string('"This is a !@#$%%%%%#%#%#% string"') == True
    assert mapper.is_string('"This is a " string"') == False

def test_identifier():
    assert mapper.is_identifier('my_var') == True
    assert mapper.is_identifier('x') == True
    assert mapper.is_identifier('_my_secret_var') == True
    assert mapper.is_identifier('____my_very_secret_var') == True
    assert mapper.is_identifier('my_fav_number_31') == True
    assert mapper.is_identifier('3cookie') == False
    assert mapper.is_identifier('_MYVAR') == True
    assert mapper.is_identifier('_MyVaR') == True
    assert mapper.is_identifier('my_var  ') == False
    assert mapper.is_identifier('my var') == False

def test_split_at_symbols():

    assert mapper._split_at_symbols('if x') == ['if x']
    assert mapper._split_at_symbols('if (x') == ['if ', '(', 'x']
    
    out = mapper._split_at_symbols('if (x < 0   ) {}')
    expected = ['if ', '(', 'x ', '<', ' 0   ', ')', ' ', '{', '', '}', '']
    assert out == expected

    assert mapper._split_at_symbols('if "hello"') == ['if "hello"']

def test_get_quotation_marks_locs():
    
    assert mapper._get_quotation_marks_locs('"Hello World"') == [0, 12]
    assert len(mapper._get_quotation_marks_locs('Helllo')) == 0
    try:
        mapper._get_quotation_marks_locs('"Helllo')
    except ValueError:
        pass
    else:
        raise Exception

def test_split_at_non_string_spaces():

    out = mapper._split_at_non_string_spaces('if "hello world" class')
    expected = ['if', '', '"hello world"', '', 'class']
    assert out == expected

    out = mapper._split_at_non_string_spaces('if "hello world" class field')
    expected = ['if', '', '"hello world"', '', 'class', 'field']
    assert out == expected

    out = mapper._split_at_non_string_spaces(
        'if class "hello world" class field')
    expected = ['if', 'class', '', '"hello world"', '', 'class', 'field']
    assert out == expected

def test_parse():

    assert mapper.parse('if x')  == ['if', 'x']
    assert mapper.parse('if (x') == ['if', '(', 'x']

    out = mapper.parse('if (x < 0   ) {}')
    expected = ['if', '(', 'x', '<', '0', ')', '{', '}']
    assert out == expected


    assert mapper.parse('while class field static') == [
        'while', 'class', 'field', 'static']

def test_parse_with_strings():
    assert mapper.parse('if "hello"') == ['if', '"hello"']
    assert mapper.parse('if "hello world"') == ['if', '"hello world"']

    out = mapper.parse('if class "hello world" class field')
    assert out == ['if', 'class', '"hello world"', 'class', 'field']

def test_analyze():

    out = mapper.analyze('if x')
    expected = '<keyword> if </keyword>\n<identifier> x </identifier>\n'
    assert out == expected

    out = mapper.analyze('while class field static')
    expected = (
        f'<keyword> while </keyword>\n'
        f'<keyword> class </keyword>\n'
        f'<keyword> field </keyword>\n'
        f'<keyword> static </keyword>\n'
    )

def _compare_list_to_file(lines: list[str], path: str):
    """
    Compares a list of strings to the contents of a file.    
    """

    with open(path) as f:
        file = f.readlines()

    for line1, line2 in zip(lines, file):
        if line1.strip() != line2.strip():
            raise ValueError(f'\nLine 1:{repr(line1)}\nLine 2:{repr(line2)}')

def test_tokenizer_with_prog():

    filepath = _get_testfile('Prog.jack')
    t = Tokenizer(filepath)
    tokens = t.tokenize().split('\n')

    compare_file = _get_testfile('Prog.xml')
    _compare_list_to_file(tokens, compare_file)

def test_tokenizer_with_square():

    filepath = _get_testfile('Square.jack')
    t = Tokenizer(filepath)
    tokens = t.tokenize().split('\n')

    with open(_get_testfile('out.xml'), 'w') as file:
        file.write(t.tokenize())

    compare_file = _get_testfile('SquareTokenizer.xml')
    _compare_list_to_file(tokens, compare_file)

def test_tokenizer_with_square_game():

    filepath = _get_testfile('SquareGame.jack')
    t = Tokenizer(filepath)
    tokens = t.tokenize().split('\n')

    with open(_get_testfile('out.xml'), 'w') as file:
        file.write(t.tokenize())

    compare_file = _get_testfile('SquareGameTokenizer.xml')
    _compare_list_to_file(tokens, compare_file)

def test_tokenizer_with_main():

    filepath = _get_testfile('Main.jack')
    t = Tokenizer(filepath)
    tokens = t.tokenize().split('\n')

    with open(_get_testfile('out.xml'), 'w') as file:
        file.write(t.tokenize())

    compare_file = _get_testfile('MainTokenizer.xml')
    _compare_list_to_file(tokens, compare_file)