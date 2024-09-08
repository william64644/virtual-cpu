import time


class RAM: 
    def __init__(self):
        """
        self.data = ["00000101"] # NOOP
        self.data += ["00001111","00000000","00000000","00000000","00000000","00000000","01010101","10101010"] # MOVIR r0f 0x55AA
        self.data += ["00001010","00001000","00000000","00000000"] # MOVRR r2f r0f
        self.data += ["00001111","00111000","00000000","00000000","00000000","00000000","00000000","00111100"] # MOVIR ref 0x38
        self.data += ["00001111","00110100","00000000","00000000","00000000","00000000","00000000","00000001"] # MOVIR rdf 0x01
        self.data += ["00010100","00111100","00110100"] # LDR rff 0x01
        self.data += ["00000100"] # HLT
        """

        """
        noop
        move 2222 into r1f
        move 0x14(20) into r2f
        store r1f at 0x14(20)
        load r3f from address 0x14(20)
        """

        self.data = ["00000101"] # NOOP
        self.data += ["00001111", "00000100", "00000000","00000000","00000000","00000000","00001000","10101110"] #MOVIR r1f 0x8AE
        self.data += ["00001111", "00001000", "00000000","00000000","00000000","00000000","00000000","00110010"] #MOVIR r2f 0x32
        self.data += ["00011001", "00000100", "00001000"] # STR r1f r2f
        self.data += ["00010100", "00001100", "00001000"] # LDR r3f r2f
        self.data += ["00000100"] # HLT
        self.data += ["00000000"] * 50


        """
        # Program to text the MOVIR instruction:
        noop
        move 1111 into r0f
        move 2222 into r1f
        move 3333 into r2f
        move 4444 into r3f
        move 6666 into r5f
        noop (10x)
        """
        """
        self.data = ["00000101"] # NOOP
        self.data += ["00001111", "00000000", "00000000","00000000","00000000","00000000","00000100","01010111"] #MOVIR r0f 0x457
        self.data += ["00001111", "00000100", "00000000","00000000","00000000","00000000","00001000","10101110"] #MOVIR r1f 0x8ae
        self.data += ["00001111", "00001000", "00000000","00000000","00000000","00000000","00001101","00000101"] #MOVIR r2f 0xd05
        self.data += ["00001111", "00001100", "00000000","00000000","00000000","00000000","00010001","01011100"] #MOVIR r3f 0x115c
        self.data += ["00001111", "00010100", "00000000","00000000","00000000","00000000","00011010","00001010"] #MOVIR r5f 0x1a0a
        self.data += ["00000100"] # HLT
        """





class CPU:
    def __init__(self, ram: RAM, heartz=1, debugMode=False):
########### Registers / RAM ###########
        self.RAM = ram
        self.heatz:float = 1 / heartz
        self.registers:dict = {
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
            "01000000": ["00000000"] * 8, #pc
        }

########### "Witchery" ###########

        self._currentInstructionFunction:function = None
        self.registerNames:list = ["r0f","r1f","r2f","r3f","r4f","r5f","r6f","r7f","r8f","r9f","raf","rbf","rcf","rdf","ref","rff"," ir"]
        self.debugMode:bool = debugMode

        self.registerNameIdMap:dict = {
            "r0f": "00000000",
            "r1f": "00000100",
            "r2f": "00001000",
            "r3f": "00001100",
            "r4f": "00010000",
            "r5f": "00010100",
            "r6f": "00011000",
            "r7f": "00011100",
            "r8f": "00100000",
            "r9f": "00100100",
            "raf": "00101000",
            "rbf": "00101100",
            "rcf": "00110000",
            "rdf": "00110100",
            "ref": "00111000",
            "rff": "00111100",
            "pc": "01000000",
            "ir": "01000011"
        }
        self.rnim:dict = self.registerNameIdMap

        self.registerIdNameMap = {
            "00000000": "r0f",
            "00000100": "r1f",
            "00001000": "r2f",
            "00001100": "r3f",
            "00010000": "r4f",
            "00010100": "r5f",
            "00011000": "r6f",
            "00011100": "r7f",
            "00100000": "r8f",
            "00100100": "r9f",
            "00101000": "raf",
            "00101100": "rbf",
            "00110000": "rcf",
            "00110100": "rdf",
            "00111000": "ref",
            "00111100": "rff"
        }
        self.rinm:dict = self.registerIdNameMap

    def overwriteArray(self, array:list, replacement:list, index:int) -> list:
        for i, item in enumerate(replacement):
            array[i+index] = item
        return array

    def registerDataToInt(self, bit_strings) -> int:
        # Combine the 8-bit strings into a single binary string
        combined_string = ''.join(bit_strings)
        
        # Convert the combined binary string to an integer
        return int(combined_string, 2)

    def intToRegisterData(self, integer):
        # Convert the integer back to a binary string, removing the '0b' prefix
        binary_string = bin(integer)[2:].zfill(64)
        
        # Split the 64-bit binary string into 8 separate 8-bit strings
        return [binary_string[i:i+8] for i in range(0, 64, 8)]

    def getIr(self)->list:
        return self.registers["01000011"]

    def getPcInt(self)->int:
        return self.registerDataToInt(self.registers["01000000"])
    
    def setPc(self, newPc:int):
        self.registers["01000000"] = self.intToRegisterData(newPc)

    def increasePc(self, increment = 1):
        self.setPc(self.getPcInt() + increment)

########### Instructions ###########

    def HLT(self):
        if self.debugMode:
            print("HLT - Haulting the CPU")

        self.increasePc()
        exit()

    def NOOP(self):
        # do nothing
        if self.debugMode:
            print("NOOP - Doing nothing")

        self.increasePc()
    
    def MOVRR(self):
        # set the value in "register A" to the value of "register B"
        instructionRegister = self.registers["01000011"]
        if self.debugMode:
            print(f"MOVRR - Moving {self.registerIdNameMap[instructionRegister[2]]} into {self.registerIdNameMap[instructionRegister[1]]}")
        
        self.registers[instructionRegister[1]] = self.registers[instructionRegister[2]]
        self.increasePc(4)

    def MOVIR(self):
        # move an imediate value into a register
        destinationRegisterId = self.registers["01000011"][1]
        registerData = self.registers["01000011"][2:8]
        if self.debugMode:
            
            print(f"MOVIR - Moving the imediate value {hex(self.registerDataToInt(registerData))} into {self.registerIdNameMap[destinationRegisterId]}")
            pass
                                                # Cant fill first 2 bytes since only 6 fit in the instruction
        self.registers[destinationRegisterId] = ["00000000","00000000"] + registerData
        self.increasePc(8)

    def LDR(self):
        destinationRegister:str = self.getIr()[1]
        registerWithMemoryAddress:str = self.getIr()[2]				
        memoryAddress:int = self.registerDataToInt(self.registers[registerWithMemoryAddress])
        self.registers[destinationRegister] = self.RAM.data[memoryAddress:memoryAddress+8]
        if self.debugMode:
            print(f"Loading {self.registerIdNameMap[destinationRegister]} with the value at {hex(memoryAddress)} (from {self.registerIdNameMap[registerWithMemoryAddress]})")
        self.increasePc(3)

    def STR(self):
        sourceRegister:str = self.getIr()[1]
        registerWithMemoryAddress:str = self.getIr()[2]				
        memoryAddress:int = self.registerDataToInt(self.registers[registerWithMemoryAddress])
        self.overwriteArray(self.RAM.data, self.registers[sourceRegister], memoryAddress)
        if self.debugMode:
            print(f"STR - Storing {hex(self.registerDataToInt(self.registers[sourceRegister]))} at {hex(memoryAddress)} {self.RAM.data[memoryAddress:memoryAddress+8]}")
        self.increasePc(3)

    def SUM(self):
        valueA = self.registerDataToInt(self.registers[self.getIr()[2]])
        valueB = self.registerDataToInt(self.registers[self.getIr()[3]])
        self.registers[self.getIr()[1]] = self.intToRegisterData(valueA + valueB)
        self.increasePc(4)

    def SUB(self):
        valueA = self.registerDataToInt(self.registers[self.getIr()[2]])
        valueB = self.registerDataToInt(self.registers[self.getIr()[3]])
        self.registers[self.getIr()[1]] = self.intToRegisterData(valueA - valueB)
        self.increasePc(4)
    def MUL(self):
        valueA = self.registerDataToInt(self.registers[self.getIr()[2]])
        valueB = self.registerDataToInt(self.registers[self.getIr()[3]])
        self.registers[self.getIr()[1]] = self.intToRegisterData(valueA * valueB)
        self.increasePc(4)

    def DIV(self):
        valueA = self.registerDataToInt(self.registers[self.getIr()[2]])
        valueB = self.registerDataToInt(self.registers[self.getIr()[3]])
        self.registers[self.getIr()[1]] = self.intToRegisterData(int(valueA / valueB))
        self.increasePc(4)

########### Decoding ###########
    decodeMap = {
        "00000100": HLT,
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
        self.logStatus() if self.debugMode else None

    def logStatus(self):
        for (name, register) in zip(cpu.registerNames, cpu.registers):
            print(name, register, cpu.registers[register], self.registerDataToInt(cpu.registers[register]) if register != "01000011" else "N.A.", hex(self.registerDataToInt(cpu.registers[register])) if register != "01000011" else "N.A.")
        print("="*109)

    def fetch(self):
                            #ir
        self.registers["01000011"] = self.RAM.data[self.getPcInt():self.getPcInt()+8]

    def decode(self):
                                                                            #ir
        self._currentInstructionFunction = self.decodeMap[self.registers["01000011"][0]]

    def execute(self):
        self._currentInstructionFunction(self)

    def clock(self):
        print("="*9,"PC:",self.getPcInt(),"="*93) if self.debugMode else None
        self.fetch()
        self.decode()
        self.execute()
        self.logStatus() if self.debugMode else None
        time.sleep(self.heatz)


ram = RAM()

cpu = CPU(ram, debugMode=True)





while True:
    cpu.clock()