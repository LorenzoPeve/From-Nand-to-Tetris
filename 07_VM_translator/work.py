from reader import Reader
import translator
import mapping
from commands import Arithmetic

def write(fname, data: list[str]):
    with open(fname, 'w') as file:
        for string in data:
            file.write(string + '\n')



fname='scrap'

# Write Translate assembly
asm_path = r'input\\' + fname + '.asm'
c = Arithmetic('sub')
data = c.translate_arithmetic()

write(asm_path, data)


# Read Assembly and Translate
r = Reader(asm_path)
data = r.read()

data = translator.translate_c_instructions(data)

# Update symbols table with labels
labels = translator.get_label_positions(data)
mapping.SYMBOL_TABLE.update(labels)

# Remove Labels
data = translator.remove_labels(data)

# Get variables
variables = translator.get_variables_locations(data, mapping.SYMBOL_TABLE)
mapping.SYMBOL_TABLE.update(variables)

data = translator.translate_a_instructions(data, mapping.SYMBOL_TABLE)

write(r'output\\' + fname + '.hack', data)