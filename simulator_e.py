
# coding: utf-8

# In[11]:


import sys
import collections
import numpy as np

# Class CPU will hold the information of the CPU
class CPU:
    PC = 0 # Program Counter
    DIC = 0 # Insturction Counter
    R = [0] * 4 # Register Values
    instructions = [] # instructions in array
    memory = [] # memory in array

def check_parity_bit(machine_line):
    # Count the number of zeros and ones
    one_zero_dict = collections.Counter(machine_line)
    # Make sure an even number of ones exist in the instructions
    if one_zero_dict["1"] % 2 == 0:
        return True
    return False

def load_program(cpu, instr_file_name, memory_file_name):
    instr_file = open(instr_file_name, "r")
    memory_file = open(memory_file_name, "r")

    for line in instr_file:
        line = line.strip()
        if len(line) < 1 or line.startswith("#") or line.startswith("U"):
            continue
        line = line.split(" ")
        cpu.instructions.append(line[0])

    for line in memory_file:
        line = line.strip()
        if len(line) < 1 or line.startswith("#"):
            continue
        number = int(line,2)
        if line.startswith("1"):
            number = (0xFFFF - int(line,2) + 1) * -1
        cpu.memory.append(number)

    for i in range(128-len(cpu.memory)):
        cpu.memory.append(0)

    instr_file.close()
    memory_file.close()

    return cpu

def run_program(cpu):
    finished = False
    while(not finished):
        instr = cpu.instructions[cpu.PC]
        if not check_parity_bit(instr):
            print(instr)
            print("ERROR: Parity Bit Error")
            sys.exit()

        if instr[1:8] == "1110111":
            cpu.R[3] = cpu.R[3] ^ cpu.R[2]
            cnt = str(bin(cpu.R[3])).count("1")
            cpu.R[3] = 16 - cnt # 16 bit integers
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:8] == "1110000":
            # Halt Command
            finished = True
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:6] == "01100":
            # AddR instruction
            Rx = registers[instr[6:8]]
            cpu.R[2] = cpu.R[Rx] + cpu.R[Rx]
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:6] == "01111":
            # AddR3 instruction
            Rx = registers[instr[6:8]]
            cpu.R[3] = cpu.R[Rx] + cpu.R[Rx]
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:6] == "01110":
            # AddR2 instruction
            Rx = registers[instr[6:8]]
            cpu.R[2] = cpu.R[2] + cpu.R[Rx]
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:6] == "01101":
            # Sub R3 instruction
            Rx = registers[instr[6:8]]
            cpu.R[3] = cpu.R[3] - cpu.R[Rx] # R3 = R3 - RX
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:4] == "001":
            # Load instruction
            Rx = registers[instr[4:6]]
            Ry = registers[instr[6:8]]
            cpu.R[Rx] = cpu.memory[cpu.R[Ry]]
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:4] == "010":
            # Store instruction
            Rx = registers[instr[4:6]]
            Ry = registers[instr[6:8]]
            cpu.memory[cpu.R[Ry]] = cpu.R[Rx]
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:4] == "000":
            # Init instruction
            Rx = registers[instr[3:5]] # Bit 4 picks whether or not this should be
            cpu.R[Rx] = int(instr[5:8], 2) # Cast the imm value into base ten
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:3] == "11":
            # Branch Equal R0
            Rx = registers[instr[3:5]]
            imm = imm_mux[instr[5:8]]
            if cpu.R[Rx] == cpu.R[0]:
            	cpu.PC = cpu.PC + imm
            else:
                cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:4] == "100":
            # Add immediate
            Rx = registers[instr[4:6]]
            imm = registers[instr[6:8]] # imm value is [0,3] in this case encoded the same way as the registers
            cpu.R[Rx] = cpu.R[Rx] + imm
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:4] == "101":
            # Set less than, if so R0 = 1
            Rx = registers[instr[4:6]]
            Ry = registers[instr[6:8]]
            if cpu.R[Rx] < cpu.R[Ry]:
                cpu.R[0] = 1
            else:
                cpu.R[0] = 0
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1

        else:
            print("Error Unknown command")
            sys.exit()
        
        
        #input("press Enter to continue...")
        #print(cpu.R)
        #print(cpu.memory[0:10])

    return cpu

registers = {"00" : 0,
             "01" : 1,
             "10" : 2,
             "11" : 3}

imm_mux = {"000": -22, # P1 jump
		   "001": -9, # P2 jump
		   "010": -5, # P1 jump
		   "011": -6, # P2(x2)
		   "100": 3, # P1 jump
		   "101": -17, # P2 jump
		   "110": 16, # P2(x3) jump
		   "111": 21} # P1 jump


if __name__ == "__main__":
    cpu1 = CPU()
    cpu1 = load_program(cpu1, "prog1_group_4_p2_bin.txt", "PatternC.txt")
    print("CPU memory 0:10", cpu1.memory[0:10])
    print(cpu1.R)
    print("Printing instructions:")
    instr = np.array(cpu1.instructions)
    print(instr[:,None])
    print("program running...")
    cpu1 = run_program(cpu1)
    print("... program finished")
    print("Registers: " + str(cpu1.R))
    print("DIC: " + str(cpu1.DIC))
    print(cpu1.memory[0:10])

