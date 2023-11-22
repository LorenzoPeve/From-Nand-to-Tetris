import os

import mapper
from tokenizer import Tokenizer

def _get_testfile(f: str) -> str:
    return os.path.join(
        os.path.dirname(__file__), 'tests', f)

def test_reader():
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
    assert mapper.is_identifier('_my_secret_var') == True
    assert mapper.is_identifier('____my_very_secret_var') == True
    assert mapper.is_identifier('my_fav_number_31') == True
    assert mapper.is_identifier('3cookie') == False
    assert mapper.is_identifier('_MYVAR') == True
    assert mapper.is_identifier('_MyVaR') == True
    assert mapper.is_identifier('my_var  ') == False
    assert mapper.is_identifier('my var') == False

def test_synthetic_line():

    assert mapper.split_at_symbols('if x') == ['if x']
    assert mapper.split_at_symbols('if (x') == ['if ', '(', 'x']
    
    out = mapper.split_at_symbols('if (x < 0   ) {}')
    expected = ['if ', '(', 'x ', '<', ' 0   ', ')', ' ', '{', '', '}', '']
    assert out == expected

    assert mapper.split_at_symbols('if "hello"') == ['if "hello"']

# def test_synthetic_line():

#     assert mapper.split_at_symbols('if x') == ['if x']
#     assert mapper.split_at_symbols('if (x') == ['if ', '(', 'x']
    
#     out = mapper.split_at_symbols('if (x < 0   ) {}')
#     expected = ['if ', '(', 'x ', '<', ' 0   ', ')', ' ', '{', '', '}', '']
#     assert out == expected


test_synthetic_line()
# def test_prog():

#     f = _get_testfile('Prog.jack')
#     with open(f) as f:
#         print(f.readlines())

