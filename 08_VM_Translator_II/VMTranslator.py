import os
from pathlib import Path
import sys

from translator import Translator
from mapper import routine_call_f

path_obj = Path(sys.argv[1])

if path_obj.is_dir():
    files = [f for f in os.listdir(path_obj) if f[-3:] == '.vm']


    # Booting: SP = 256
    asm_code = '@256\nD=A\n@0\nM=D\n'
    # Calling Sys.init
    asm_code += routine_call_f('Sys.init', 0, 0)

    for file in files:
        t = Translator(os.path.join(path_obj, file))
        asm_code += t.translate()

    asm_code = asm_code + '(END)\n@END\n0;JMP\n'

    # Output to same directory
    out_path = os.path.join(path_obj, f'{path_obj.name}.asm')
    with open(out_path, "w") as file:
        file.write(asm_code)

elif path_obj.is_file():

    t = Translator(path_obj)    
    asm_code = t.translate()
    asm_code = asm_code + '(END)\n@END\n0;JMP\n'
    
    out_path = os.path.join(os.path.dirname(path_obj), f'{path_obj.stem}.asm')
    with open(out_path, "w") as file:
        file.write(asm_code)