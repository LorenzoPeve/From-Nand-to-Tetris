import sys
import os

from reader import Reader
from operations import Operation
from memory import  MemorySegment


if len(sys.argv[1].split('.')) > 1:

    r = Reader(sys.argv[1])
    fname = sys.argv[1].split('.')[0]
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

else:
    
    files=  [f for f in os.listdir(sys.argv[1]) if f[-3:] == '.vm']

    for file in files:
        
        # Read file
        r = Reader(os.path.join(sys.argv[1], file))
        fname = file.split('.')[0]
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
    
        translated = [t for t in translated if len(t)>1]
        translated.extend(['(END)', '@END', '0;JMP']) # Infinite loop

        with open(os.path.join(sys.argv[1], fname) + '.asm', 'w') as file:
            for i, string in  enumerate(translated):
                if i == len(translated)-1:
                    file.write(string)
                    continue
                file.write(string + '\n')

with open(fname + '.asm', 'w') as file:
    for i, string in  enumerate(translated):
        if i == len(translated)-1:
            file.write(string)
            continue
        file.write(string + '\n')