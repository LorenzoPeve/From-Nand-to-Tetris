import os
from pathlib import Path
import sys

from translator import Translator

path_obj = Path(sys.argv[1])

if path_obj.is_dir():
    files = [f for f in os.listdir(path_obj) if f[-3:] == '.vm']

    asm_code = ""
    for file in files:
        t = Translator(os.path.join(path_obj, file))
        asm_code += t.translate()

    asm_code = asm_code + '(END)\n@END\n0;JMP\n'
    with open(f'{path_obj.name}.asm', "w") as file:
        file.write(asm_code)

elif path_obj.is_file():

    t = Translator(path_obj)
    asm_code = t.translate()
    asm_code = asm_code + '(END)\n@END\n0;JMP\n'
    
    with open(f'{path_obj.stem}.asm', "w") as file:
        file.write(asm_code)