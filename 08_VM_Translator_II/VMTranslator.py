import sys
import os

from reader import Reader
from operations import Operation
from memory import MemorySegment
from branching import  Branch
from functions import Function


def _get_filename(filepath) -> str:
    return os.path.basename(filepath)


def _write_new_file_with_extension(filepath, data):
    """
    Writes a new file with the same name as the given file and
    ".asm" extension.
    """
    filename, _ = os.path.splitext(filepath)
    new_path = filename + '.asm'

    with open(new_path, "w") as file:
        for i, string in enumerate(data):
            if i == len(data)-1:
                file.write(string)
                continue
            file.write(string + '\n')


def _is_arith_operation(s: str) -> bool:
    """Returns True if line is an arithmetic operation."""
    if s in Operation.allowed:
        return True
    return False


def _is_memory_alloc(s: str) -> bool:
    """Returns True if line is a memory operation."""
    if s.startswith('push') or s.startswith('pop'):
        return True
    return False


def _is_function(s: str) -> bool:
    """Returns True if line is a function definition or function call."""
    if s.startswith('call') or s.startswith('function'):
        return True
    return False


def _is_branching_step(s: str) -> bool:
    """Returns True if line is a branching command."""
    if (s.startswith('label') or
        s.startswith('if-goto') or
            s.startswith('goto')):

        return True
    return False


def translate_file(filepath: str):  # -> list[str]
    """Initializes reader and translates a .vm file into a list[str]"""
    r = Reader(filepath)
    fname = _get_filename(filepath)
    data = r.read()

    translated = []
    for line in data:
        translated.append(f'// {line}')

        if _is_arith_operation(line):
            op = Operation(line)
            t = op.translate_operations()

        elif _is_memory_alloc(line):
            m = MemorySegment(line, fname)
            t = m.translate_memory()

        elif _is_branching_step(line):
            b = Branch(line)
            t = b.translate_branch()

        elif _is_branching_step(line):
            f = Function(line)
            t = f.translate_branch()

        else:
            raise Exception(f'Line couldnt be translated: {line}')

        translated.extend(t)

    translated = [t for t in translated if t != '']
    return translated


is_dir = os.path.isdir(sys.argv[1])

if not is_dir:

    translated = translate_file(sys.argv[1])
    translated.extend(['(END)', '@END', '0;JMP'])  # Infinite loop
    print(translated)
    _write_new_file_with_extension(sys.argv[1], translated)

# if len(sys.argv[1].split('.')) > 1:


#     translated = [t for t in translated if t != '']
#     translated.extend(['(END)', '@END', '0;JMP']) # Infinite loop


# with open(fname + '.asm', 'w') as file:
#     for i, string in  enumerate(translated):
#         if i == len(translated)-1:
#             file.write(string)
#             continue
#         file.write(string + '\n')
