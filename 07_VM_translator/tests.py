import os
from reader import Reader

def test_remove_whitespace_within():

    data = [
        "    hello    world   ",
        "  this   is  a test  ",
        "multiple\nlines\n   with\ttabs   "
    ]
    r = Reader('')
    out = r.remove_whitespace_within(data)
    assert out == ['hello world', 'this is a test', 'multiple lines with tabs']

test_remove_whitespace_within()