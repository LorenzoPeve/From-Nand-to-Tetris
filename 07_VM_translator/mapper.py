"""
Pointer-based access is realized by:
    @arr   // We want the address stored @arr
    A=M

Arithmetic Operations follow the same protocol:
    - Use heavily RAM[13-15] as general purpose registers for storing operands
    - Set D-register to the result of the computation

"""
import re

MEMSEGMENTS = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT'
}
PUSH_MEMOP = re.compile(r'push (?P<segment>local|argument|this|that) (?P<value>\d+)')
POP_MEMOP = re.compile(r'pop (?P<segment>local|argument|this|that) (?P<value>\d+)')



def increment_stack_pointer():
    """RAM[0] = RAM[0] + 1"""
    return '@SP\nM=M+1\n'

def decrement_stack_pointer():
    """RAM[0] = RAM[0] - 1"""
    return '@SP\nM=M-1\n'

def _push_d_to_stack():
    """
    This is a convenience method that pushes the contents of D-register onto
    the stack and increments the stack pointer.
    
    This allows for all the arithmetic and memory operation to unload their
    "result" in D and call this method to take it to the stack.
    """
    return (
        f'@SP\n' # pointer-based access
        f'A=M\n'
        f'M=D\n' # push constant to stack
    )

def _pop_from_stack_to_i(i: int):
    """Pops from stack and stores the popped value into RAM[i]."""
    return (
        f'{decrement_stack_pointer()}'
        f'A=M\n'
        f'D=M\n'
        f'@{i}\n'
        f'M=D\n'
) 

def arop_add():
    """
    Pushes operand onto RAM[13] and RAM[14] and pushes the result of 
    RAM[13]+RAM[14] to the stack
    """
    return (
        f'{_pop_from_stack_to_i(13)}'
        f'{_pop_from_stack_to_i(14)}'
        f'@13\n'
        f'D=M\n'
        f'@14\n'
        f'D=D+M\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def arop_sub():
    """
    Pushes operand onto RAM[13] and RAM[14] and pushes the result of 
    RAM[13]-RAM[14] to the stack

        push constant 2
        push constant 7
        sub
        >>> -5   
    """
    return (
        f'{_pop_from_stack_to_i(14)}'
        f'{_pop_from_stack_to_i(13)}'
        f'@13\n'
        f'D=M\n'
        f'@14\n'
        f'D=D-M\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def arop_neg():
    """
    Pushes to the stack -x, where x is the last value pushed into the stack.   
    """
    return (
        f'{_pop_from_stack_to_i(13)}'
        f'@13\n'
        f'D=-M\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def arop_not():
    """
    Pushes to the stack !x, where x is the last value pushed into the stack.   
    """
    return (
        f'{_pop_from_stack_to_i(13)}'
        f'@13\n'
        f'D=!M\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def arop_or():
    """Performs bitwise x OR y."""
    return (
        f'{_pop_from_stack_to_i(14)}'
        f'{_pop_from_stack_to_i(13)}'
        f'@13\n'
        f'D=M\n'
        f'@14\n'
        f'D=D|M\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def arop_and():
    """Performs bitwise x AND y."""
    return (
        f'{_pop_from_stack_to_i(14)}'
        f'{_pop_from_stack_to_i(13)}'
        f'@13\n'
        f'D=M\n'
        f'@14\n'
        f'D=D&M\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def arop_eq(i: int):
    """Performs equality comparison."""
    return (
        f'{_pop_from_stack_to_i(14)}'
        f'{_pop_from_stack_to_i(13)}'

        f'@13\n'
        f'D=M\n'
        f'@14\n'
        f'D=D-M\n'
        f'@NOT_EQ_{i}\n' # IF EQ, jump to not EQ
        f'D;JNE\n'

        f'D=-1\n'
        f'{_push_d_to_stack()}'
        f'@END_EQ_{i}\n'
        f'0;JMP\n'

        f'(NOT_EQ_{i})\n'
        f'D=0\n'
        f'{_push_d_to_stack()}'

        f'(END_EQ_{i})\n'
        f'{increment_stack_pointer()}'
    )

def arop_gt(i: int):
    """Evaluates if x > y is True. @R13 stores x and @R14 stores y."""
    return (
        f'{_pop_from_stack_to_i(14)}'
        f'{_pop_from_stack_to_i(13)}'
        f'@R13\n'
        f'D=M\n'

        f'@X_LESS_THAN_ZERO{i}\n'
        f'D; JLT\n'

        # x >= 0
        f'@R14\n'
        f'D=M\n'
        f'@SAME_SIGN{i}\n'
        f'D; JGE\n'

        # # x >= 0 and y < 0. Thus, x > y
        f'@IS_TRUE_{i}\n'
        f'0; JMP\n'

        # x < 0
        f'(X_LESS_THAN_ZERO{i})\n'
        f'@R14\n'
        f'D=M\n'
        f'@SAME_SIGN{i}\n'
        f'D; JLT\n'

        # x < 0 and y >= 0. Thus, x < y
        f'@IS_FALSE_{i}\n'
        f'0; JMP\n'

        # If (x>=0 and y>=0) or (x<0 and y<0)
        f'(SAME_SIGN{i})\n'
        f'@R13\n' 
        f'D=M\n'  # D = x
        f'@R14\n'
        f'D=D-M\n' # D = x-y. If D > 0, x is greater than y
        f'@IS_TRUE_{i}\n'
        f'D; JGT\n'

        f'(IS_FALSE_{i})\n'
        f'D=0\n'
        f'@END_GT_{i}\n'
        f'0; JMP\n'

        f'(IS_TRUE_{i})\n'
        f'D=-1\n'
           
        f'(END_GT_{i})\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def arop_lt(i: int):
    
    """Evaluates if x < y is True. @R13 stores x and @R14 stores y."""
    return (
        f'{_pop_from_stack_to_i(14)}'
        f'{_pop_from_stack_to_i(13)}'
        f'@R13\n'
        f'D=M\n'

        f'@X_LESS_THAN_ZERO{i}\n'
        f'D; JLT\n'

        # x >= 0
        f'@R14\n'
        f'D=M\n'
        f'@SAME_SIGN{i}\n'
        f'D; JGE\n'

        # # x >= 0 and y < 0. Thus, x > y
        f'@IS_FALSE_{i}\n'
        f'0; JMP\n'

        # x < 0
        f'(X_LESS_THAN_ZERO{i})\n'
        f'@R14\n'
        f'D=M\n'
        f'@SAME_SIGN{i}\n'
        f'D; JLT\n'

        # x < 0 and y >= 0. Thus, x < y
        f'@IS_TRUE_{i}\n'
        f'0; JMP\n'

        # If (x>=0 and y>=0) or (x<0 and y<0)
        f'(SAME_SIGN{i})\n'
        f'@R13\n' 
        f'D=M\n'  # D = x
        f'@R14\n'
        f'D=D-M\n' # D = x-y. If D < 0, x is less than y
        f'@IS_TRUE_{i}\n'
        f'D; JLT\n'

        f'(IS_FALSE_{i})\n'
        f'D=0\n'
        f'@END_LT_{i}\n'
        f'0; JMP\n'

        f'(IS_TRUE_{i})\n'
        f'D=-1\n'
           
        f'(END_LT_{i})\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def push_constant_to_stack(i: int):
    return (
        f'@{i}\n'
        f'D=A\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def push_from_segment(segment: str, index: int):
    """
    Pushes a value from one of LCL, ARG, THIS, THAT memory segments into the
    stack.
    """
    return (
        f'@{index}\n'
        f'D=A\n'
        f'@{segment}\n'
        f'A=M+D\n'
        f'D=M\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def pop_from_segment(segment: str, index: int):
    """
    Pops a value from the stack into one of LCL, ARG, THIS, THAT memory
    segments.

    Puts target address into R13.
    """    
    return (
        # addr = segment_base + i
        f'@{index}\n'
        f'D=A\n'
        f'@{segment}\n'
        f'D=D+M\n'
        f'@13\n'
        f'M=D\n'

        f'{decrement_stack_pointer()}'

        # Set D-register to *SP
        f'@SP\n'
        f'A=M\n'
        f'D=M\n'

        # RAM[addr] = D-register
        f'@13\n'
        f'A=M\n'
        f'M=D\n'
    )

def push_from_temp(index: int):    
    return (
        f'@{5+index}\n'
        f'D=M\n'
        f'{_push_d_to_stack()}'
        f'{increment_stack_pointer()}'
    )

def pop_from_temp(index: int):    
    return (
        f'{decrement_stack_pointer()}'
        # Set D-register to *SP
        f'@SP\n'
        f'A=M\n'
        f'D=M\n'

        f'@{5+index}\n'
        f'M=D\n'
    )

def translate_line(line: str, line_number: int):
       
    if line.startswith('push constant'):
        i = int(line.replace('push constant', '').strip())
        return push_constant_to_stack(i)
    
    elif line.startswith('add'):
        return arop_add()
    
    elif line.startswith('sub'):
        return arop_sub()
    
    elif line.startswith('neg'):
        return arop_neg()
    
    elif line.startswith('not'):
        return arop_not()
    
    elif line.startswith('or'):
        return arop_or()

    elif line.startswith('and'):
        return arop_and()

    elif line.startswith('eq'):
        return arop_eq(line_number)
    
    elif line.startswith('gt'):
        return arop_gt(line_number)
    
    elif line.startswith('lt'):
        return arop_gt(line_number)

    elif PUSH_MEMOP.match(line):
        m = PUSH_MEMOP.match(line)
        segment = MEMSEGMENTS[m.group('segment')]
        index = m.group('value')
        return push_from_segment(segment, index)
    
    elif POP_MEMOP.match(line):
        m = POP_MEMOP.match(line)
        segment = MEMSEGMENTS[m.group('segment')]
        index = m.group('value')
        return pop_from_segment(segment, index)
    
    elif line.startswith('push temp'):
        i = int(line.replace('push temp', '').strip())
        assert i >= 0 and i <=7, f'Temp only goes 5-12'
        return push_from_temp(i)
    
    elif line.startswith('pop temp'):
        i = int(line.replace('pop temp', '').strip())
        assert i >= 0 and i <=7, f'Temp only goes 5-12'
        return pop_from_temp(i)


    else:
        raise ValueError(f'Unrecognizable line {line}')
