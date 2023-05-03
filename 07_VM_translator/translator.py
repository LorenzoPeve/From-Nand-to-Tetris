import re

import mapping


def translate_c_instructions(data: list[str]) -> None:
    """Translates all the C-instructions by splitting and mapping."""
    for i, line in enumerate(data):
        if line.startswith('@') or line.startswith('('):
            continue
        else:
            d = _parse_c_instruction(line)
            data[i] = _map_c_instruction(d)
    return data


def _parse_c_instruction(s: str):
    """Splits a C-instruction into a dictionary with [dest, comp, jump] keys"""

    match = re.match(r'(\w+)=([^;]+);(\w+)', s)
    if match:
        return {
            'dest': match.group(1),
            'comp': match.group(2),
            'jump': match.group(3)
        }

    match = re.match(r'(\w+)=([^;]+)', s)
    if match:
        return {
            'dest': match.group(1),
            'comp': match.group(2),
            'jump': None
        }

    match = re.match(r'([^;]+);(\w+)', s)
    if match:
        return {
            'dest': None,
            'comp': match.group(1),
            'jump': match.group(2)
        }


def _map_c_instruction(d: dict) -> str:
    """
    Returns the binary representation of the C-instruction by mapping each of
    the components.
    """
    ins = (
        f"111"
        f"{mapping.COMP[d['comp']]}"
        f"{mapping.DEST[d['dest']]}"
        f"{mapping.JUMPS[d['jump']]}"
    )
    assert len(ins) == 16
    return ins


def _get_binary_code(num) -> str:
    """Gets the 15-bit binary representation of a number"""
    binary_code = format(num, "015b")
    if len(binary_code) > 15:
        raise ValueError(f'Converting {num} to binary resulted in overflow.')
    return binary_code


def get_label_positions(data: list[str]) -> dict:
    """Gets the instruction location for each (LABEL)."""

    labels = {}
    is_label = re.compile(r"\(\w+\)")
    counter = 0
    for line in data:
        if not is_label.match(line):
            counter += 1
            continue
        else:
            name = line[1:-1]
            labels[name] = counter
    return labels


def remove_labels(data: list[str]) -> list[str]:
    """Removes (LABEL) from the instruction."""
    program_w_no_labels = []
    is_label = re.compile(r"\(.+\)")
    for line in data:
        if is_label.match(line):
            continue
        else:
            program_w_no_labels.append(line)
    return program_w_no_labels


def get_variables_locations(data: list[str], pre_def_symbols: dict) -> dict:
    """
    Returns a dictionary with memory locations for variables that are not
    predefined symbols.
    """
    variables = {}
    is_symbol = re.compile(r"@[^\d]\w+")  # anything that doesnt start with #
    mem_loc = 16
    for line in data:
        if (is_symbol.match(line) and
            line[1:] not in variables and
                line[1:] not in pre_def_symbols):

            variables[line[1:]] = mem_loc
            mem_loc += 1

    return variables


def translate_a_instructions(data: list[str], symbols: dict) -> None:
    """Translates @17 into 0000000000010001"""

    is_constant = re.compile(r"@\d+")
    is_symbol = re.compile(r"@\w+")
    for i, line in enumerate(data):
        if i == 136:
            print('here')

        if is_constant.match(line):
            data[i] = '0' + _get_binary_code(int(line[1:]))
        elif is_symbol.match(line) and line[1:] in symbols:
            num = symbols[line[1:]]
            data[i] = '0' + _get_binary_code(num)

    return data


assert translate_c_instructions(['MD=D+1'])[0] == '1110011111011000'
assert translate_a_instructions(
    ['@17'], mapping.SYMBOL_TABLE)[0] == '0000000000010001'
assert translate_a_instructions(
    ['@55'], mapping.SYMBOL_TABLE)[0] == '0000000000110111'
assert translate_a_instructions(
    ['@R0'], mapping.SYMBOL_TABLE)[0] == '0000000000000000'
assert translate_a_instructions(
    ['@SCREEN'], mapping.SYMBOL_TABLE)[0] == '0100000000000000'
assert translate_a_instructions(
    ['@KBD'], mapping.SYMBOL_TABLE)[0] == '0110000000000000'