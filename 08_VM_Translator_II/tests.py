from reader import Reader
from memory import  MemorySegment
from branching import  Branch
from functions import Function

def test_remove_whitespace_within():

    data = [
        "    hello    world   ",
        "  this   is  a test  ",
        "multiple\nlines\n   with\ttabs   "
    ]
    r = Reader('')
    out = r.remove_whitespace_within(data)
    assert out == ['hello world', 'this is a test', 'multiple lines with tabs']



c = MemorySegment('push constant 5', 'hey')
assert c.op == 'push'
assert c.segment == 'constant'
assert c.i == 5


# b = Branch('label LOOP_START')
# print(b.translate_branch())

# b = Branch('goto END_LOOP')
# print(b.translate_branch())

# f = Function('function mult 2')
# print(f.translate())

f = Function('return')
data = f.translate()

with open('test.txt', "w") as file:
    for i, string in enumerate(data):
        if i == len(data)-1:
            file.write(string)
            continue
        file.write(string + '\n')