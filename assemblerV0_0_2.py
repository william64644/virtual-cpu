def assemble(assembly:str):
    registerNameIdMap:dict = {
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

    compiledBinary = []

    for line in assembly.splitlines():
        instruction = line.split(' ')
        opcode = instruction[0].lower()
        if opcode == "hlt":
            compiledBinary += ["00000100"]
        elif opcode == "noop":
            compiledBinary += ["00000101"]
        elif opcode == "movrr":
            compiledBinary += ["00001010", registerNameIdMap[instruction[1]], registerNameIdMap[instruction[2]], registerNameIdMap[instruction[3]]]
        elif opcode == "movir":
            compiledBinary += ["00001111", registerNameIdMap[instruction[1]]]

            immediateValueInt = int(instruction[2], 0)

            # Convert the integer back to a binary string, removing the '0b' prefix
            binary_string = bin(immediateValueInt)[2:].zfill(48)
            
            # Split the 64-bit binary string into 8 separate 8-bit strings
            bytesList = [binary_string[i:i+8] for i in range(0, 48, 8)]

            compiledBinary += bytesList

        elif opcode == "ldr":
            compiledBinary += ["00010100", registerNameIdMap[instruction[1]], registerNameIdMap[instruction[2]]]
        elif opcode == "str":
            compiledBinary += ["00011001", registerNameIdMap[instruction[1]], registerNameIdMap[instruction[2]]]
        elif opcode == "sum":
            compiledBinary += ["00011110", registerNameIdMap[instruction[1]], registerNameIdMap[instruction[2]], registerNameIdMap[instruction[3]]]
        elif opcode == "sub":
            compiledBinary += ["00100011", registerNameIdMap[instruction[1]], registerNameIdMap[instruction[2]], registerNameIdMap[instruction[3]]]
        elif opcode == "mul":
            compiledBinary += ["00101000", registerNameIdMap[instruction[1]], registerNameIdMap[instruction[2]], registerNameIdMap[instruction[3]]]
        elif opcode == "div":
            compiledBinary += ["00101101", registerNameIdMap[instruction[1]], registerNameIdMap[instruction[2]], registerNameIdMap[instruction[3]]]

    return compiledBinary