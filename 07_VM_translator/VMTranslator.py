import sys

from reader import Reader
from operations import Operation
from memory import  MemorySegment




r = Reader(sys.argv[1])

# import os
# print(os.listdir())
# r = Reader(r'.\07_VM_translator\input\lp_test.vm')
# fname=sys.argv[1].split('\\')[1][:-3]


print(f'Input File {sys.argv[1]}')
fname = sys.argv[1].split('.')[0]
print(f'Name {fname}')
data = r.read()

translated = []
for line in data:
    translated.append(f'// {line}')
    try:
        op = Operation(line)
        t = op.translate_operations()

    except ValueError as e:
        try:
            m = MemorySegment(line, fname)
            t = m.translate_memory()
        except Exception as e:
            raise Exception
    finally:
        translated.extend(t)

translated = [t for t in translated if t != '']
translated.extend(['(END)', '@END', '0;JMP']) # Infinite loop

with open(fname + '.asm', 'w') as file:
    for i, string in  enumerate(translated):
        if i == len(translated)-1:
            file.write(string)
            continue
        file.write(string + '\n')

with open(fname + '.asm', 'r') as file:
    print(file.readlines())