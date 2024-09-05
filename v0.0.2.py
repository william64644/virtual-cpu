import time

class RAM: 
    def __init__(self):
        self.data = ["00000101"] # NOOP
        self.data += ["00001111","00000000","00000000","00000000","00000000","00000000","01010101","10101010"] # MOVIR r0f 0x55AA
        self.data += ["00001010","00001000","00000000","00000000"] # MOVRR r2f r0f
        #self.data += ["00000101"] * 50 # NOOP * 50

class CPU:
    def __init__(self, ram, heartz=1):
########### Registers / RAM ###########
        self.RAM = ram
        self.heatz = 1 / heartz
        self.registers = {
            "00000000": ["00000000"] * 8, #r0f
            "00000100": ["00000000"] * 8, #r1f
            "00001000": ["00000000"] * 8, #r2f
            "00001100": ["00000000"] * 8, #r3f
            "00010000": ["00000000"] * 8, #r4f
            "00010100": ["00000000"] * 8, #r5f
            "00011000": ["00000000"] * 8, #r6f
            "00011100": ["00000000"] * 8, #r7f
            "00100000": ["00000000"] * 8, #r8f
            "00100100": ["00000000"] * 8, #r9f
            "00101000": ["00000000"] * 8, #raf
            "00101100": ["00000000"] * 8, #rbf
            "00110000": ["00000000"] * 8, #rcf
            "00110100": ["00000000"] * 8, #rdf
            "00111000": ["00000000"] * 8, #ref
            "00111100": ["00000000"] * 8, #rff

            "01000011": ["00000000"] * 8, #ir
        }

        self.pc = 0


########### "Witchery" ###########

        self._currentInstructionFunction = None

        self.registerNames =["r0f","r1f","r2f","r3f","r4f","r5f","r6f","r7f","r8f","r9f","raf","rbf","rcf","rdf","ref","rff"," ir"]

########### Instructions ###########

    def NOOP(self):
        self.pc += 1
    
    def MOVRR(self):
        self.registers[self.registers["01000011"][1]] = self.registers[self.registers["01000011"][2]]
        self.pc += 4

    def MOVIR(self):
        self.registers[self.registers["01000011"][1]] = ["00000000","00000000"] + self.registers["01000011"][2:8]
        self.pc += 8

    def LDR(self):
        pass

    def STR(self):
        pass

    def SUM(self):
        pass

    def SUB(self):
        pass

    def MUL(self):
        pass

    def DIV(self):
        pass

########### Decoding ###########
    decodeMap = {
        "00000101": NOOP,
        "00001010": MOVRR,
        "00001111": MOVIR,
        "00010100": LDR,
        "00011001": STR,
        "00011110": SUM,
        "00100011": SUB,
        "00101000": MUL,
        "00101101": DIV
    }

########### Routine ###########

    def initialize(self):
        pass

    def logStatus(self):
        print()
        print("="*9,"PC:",self.pc,"="*93)
        for (name, register) in zip(cpu.registerNames, cpu.registers):
            print(name, register, cpu.registers[register])
        print("="*109)

    def fetch(self):
                            #ir
        self.registers["01000011"] = self.RAM.data[self.pc:self.pc+8]

    def decode(self):
                                                                            #ir
        self._currentInstructionFunction = self.decodeMap[self.registers["01000011"][0]]

    def execute(self):
        self._currentInstructionFunction(self)

    def clock(self):
        self.fetch()
        self.decode()
        self.execute()
        time.sleep(self.heatz)


ram = RAM()

cpu = CPU(ram)


cpu.logStatus()
cpu.clock()
cpu.logStatus()
cpu.clock()
cpu.logStatus()
cpu.clock()
cpu.logStatus()
