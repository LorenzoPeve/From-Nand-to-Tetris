from reader import Reader
from memory import  MemorySegment

def test_remove_whitespace_within():

    data = [
        "    hello    world   ",
        "  this   is  a test  ",
        "multiple\nlines\n   with\ttabs   "
    ]
    r = Reader('')
    out = r.remove_whitespace_within(data)
    assert out == ['hello world', 'this is a test', 'multiple lines with tabs']



c = MemorySegment('push constant 5')
assert c.op == 'push'
assert c.segment == 'constant'
assert c.i == 5