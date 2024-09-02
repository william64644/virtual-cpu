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
    #data = ['0']*BYTE_SIZE*ROM_BYTES
    data = ['0']*7
    data.extend('1')
    data.extend(['0']*56)
    data.extend(data)
    data.extend(data)
    data.extend(data)
    data.extend(data)

class CPU:
    def __init__(self):
        self.instructionBrute = []
        self.decodedFunction = None
        self.opcode = ''
        self.r0 = ['0']*REGISTER_SIZE
        self.r1 = ['0']*REGISTER_SIZE
        self.r2 = ['0']*REGISTER_SIZE
        self.r3 = ['0']*REGISTER_SIZE
        self.r4 = ['0']*REGISTER_SIZE
        self.r5 = ['0']*REGISTER_SIZE
        self.r6 = ['0']*REGISTER_SIZE
        self.r7 = ['0']*REGISTER_SIZE
        self.pc = ['0']*REGISTER_SIZE
        
    def _increasePc(self):
        print('='*64)
        print("pc was: ", self.pc)
        pcInt = int(''.join(self.pc),2)
        pcInt += 1
        pcString = "{0:b}".format(pcInt)
        pcString = '0'*(64-len(pcString)) + pcString
        self.pc = list(pcString)
        print('='*64)
        print("now pc is: ", self.pc)
        print('='*64)
        
    def MOVRR(self):
        pass
    
    def MOVIR(self):
        pass
        
    def fetch(self):
        pcInt = int(''.join(self.pc),2)
        self.instructionBrute = ROM.data[pcInt*64:pcInt*64+63]
    
    decodeMap = {
        "00000001": MOVRR,
        "00000010": MOVIR
    }
    
    def decode(self):
        self.opcode = ''.join(self.instructionBrute[:8])
        self.decodedFunction = self.decodeMap[self.opcode]

    def execute(self):
        self.decodedFunction(self)
        
        self._increasePc()

    def clock(self):
        self.fetch()
        self.decode()
        self.execute()
        
        
        
print("FULL ROM:")
print(ROM.data) 
cpu = CPU()

cpu.clock()
cpu.clock()
cpu.clock()
cpu.clock()