from reader import Reader
import translator
import mapping

def write(fname, data: list[str]):
    with open(r'output\\' + fname + '.hack', 'w') as file:
        for string in data:
            file.write(string + '\n')
        

fname='Rect'
#r = Reader(r'06_Assembler\input\\' + fname + '.asm')
r = Reader(r'input\\' + fname + '.asm')
data = r.read()

data = translator.translate_c_instructions(data)
#write('Pong_C', data)

# Update symbols table with labels
labels = translator.get_label_positions(data)
mapping.SYMBOL_TABLE.update(labels)

# Remove Labels
data = translator.remove_labels(data)
#write('Pong_labels_removed', data)

# Get variables
variables = translator.get_variables_locations(data, mapping.SYMBOL_TABLE)
mapping.SYMBOL_TABLE.update(variables)

data = translator.translate_a_instructions(data, mapping.SYMBOL_TABLE)
write(fname, data)