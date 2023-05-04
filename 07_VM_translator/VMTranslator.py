import sys

from reader import Reader
from operations import Operation
from memory import  MemorySegment

def write(fname, data: list[str]):
    with open(fname, 'w') as file:
        for string in data:
            file.write(string + '\n')

r = Reader(sys.argv[1])
data = r.read()

translated = []
for line in data:

    try:
        op = Operation(line)
        t = op.translate_operations()

    except ValueError as e:
        try:
            m = MemorySegment(line)
            t = m.translate_memory()
        except Exception as e:
            print(f'Line: {line}')
            print(e)
    finally:
        translated.extend(t)

translated = [t for t in translated if t != '']
translated.extend(['(END)', '@END', '0;JMP']) # Infinite loop

write(r'output\\' + sys.argv[1].split('\\')[1][:-3] + '.asm', translated)

