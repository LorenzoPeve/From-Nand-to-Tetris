"""
Pointer-based access is realized by:
    @arr   // We want the address stored @arr
    A=M

Arithmetic Operations follow the same protocol:
    - Use heavily RAM[13-15] as general purpose registers for storing operands
    - Set D-register to the result of the computation

"""


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
        f'{_pop_from_stack_to_i(13)}'
        f'{_pop_from_stack_to_i(14)}'
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
        f'{_pop_from_stack_to_i(13)}'
        f'{_pop_from_stack_to_i(14)}'
        f'@13\n'
        f'D=M\n'
        f'@14\n'
        f'D=D|M\n'
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

def translate_line(line: str):
    
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

    else:
        raise ValueError()
