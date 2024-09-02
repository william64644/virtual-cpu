""" INSTRUCTION SET:
MOV - immediate value to register
8 bits->opcode() | 3 bits->inRegister | 3 bits->outRegister | 50 bits->immediate value



"""


BYTE_SIZE = 8
RAM_BYTES = 32
ROM_BYTES = 32
REGISTER_SIZE = 64

class RAM:
    
    data = ['0']*BYTE_SIZE*RAM_BYTES


class ROM:
    data = ['0']*BYTE_SIZE*ROM_BYTES

class CPU:
    r0 = ['0']*REGISTER_SIZE
    r1 = ['0']*REGISTER_SIZE
    r2 = ['0']*REGISTER_SIZE
    r3 = ['0']*REGISTER_SIZE
    r4 = ['0']*REGISTER_SIZE
    r5 = ['0']*REGISTER_SIZE
    r6 = ['0']*REGISTER_SIZE
    r7 = ['0']*REGISTER_SIZE


print('1'*16)