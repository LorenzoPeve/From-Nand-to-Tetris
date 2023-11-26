import os

from tokenizer import Tokenizer
from grammar import Compiler

def test_init():

    t = Tokenizer(stream=['let count = count + 1;'])
    tokens = t.tokenize(headers='').split('\n')[:-1]
    c = Compiler(tokens=tokens)
    assert len(c.tokens) == 7

def test_get_tag_and_body():

    c = Compiler(None)
    tag, body = c.get_tag_and_body('<identifier> count </identifier>')
    assert tag == 'identifier'
    assert body == 'count'

    try:
        tag, body = c.get_tag_and_body('<symbol></symbol>')
    except AttributeError as e:
        assert e.args[0] == "'NoneType' object has no attribute 'group'"

def test_get_identifier():

    c = Compiler(None)
    varname = c.get_identifier_term('<identifier> count </identifier>')
    assert varname == 'count'
    varname = c.get_identifier_term('<symbol> * </symbol>')
    assert varname is None

def test_get_constant():

    c = Compiler(None)
    varname = c.get_integerconstant_term('<integerConstant> 12 </integerConstant>')
    assert varname == '12'

def _get_testfile(f: str) -> str:
    return os.path.join(
        os.path.dirname(__file__), 'tests', f)

def _compare_list_to_file(lines: list[str], path: str):
    """
    Compares a list of strings to the contents of a file.    
    """

    with open(path) as f:
        file = f.readlines()

    for line1, line2 in zip(lines, file):
        if line1.strip() != line2.strip():
            raise ValueError(f'\nLine 1:{repr(line1)}\nLine 2:{repr(line2)}')

def test_let():

    t = Tokenizer(stream=['let count = count + 1;'])
    tokens = t.tokenize(headers='').split('\n')[:-1]
    c = Compiler(tokens=tokens)
    c.compile()
    tokens = c.compiled_pg.split('\n')

    with open(_get_testfile('out.xml'), 'w') as file:
        file.write(c.compiled_pg)

    compare_file = _get_testfile('./test_without_expressions/let.xml')
    _compare_list_to_file(tokens, compare_file)