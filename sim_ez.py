
# coding: utf-8

# In[4]:


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

def convert_imm_value(number):
    if number < 0:
        number = 0xFFFF + number + 1
    return format(int(number), "016b")

def xor(a, b):
    result = ""
    for c,d in zip(a,b):
        if c == d:
            result = result + "0"
        else:
            result = result + "1"
    return result

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
            '''
            cpu.R[3] = cpu.R[3] ^ cpu.R[2]
            cnt = str(bin(cpu.R[3])).count("1")
            cpu.R[3] = 16 - cnt # 16 bit integers
            '''
            a = convert_imm_value(cpu.R[3])
            b = convert_imm_value(cpu.R[2])
            result = collections.Counter(xor(a,b))
            cpu.R[3] = result["0"]
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

        #print(cpu.R)
        #print(cpu.memory[0:10])

    return cpu

registers = {"00" : 0,
             "01" : 1,
             "10" : 2,
             "11" : 3}

imm_mux = {"000": -22,          #P1 JMP
		   "001": -9,   #P2 JMP
		   "010": -5,   #P1 JMP
		   "011": -6,   #P2 JMP (X2)
		   "100": 3,    #P1 JMP
		   "101": -17,  #P2 JMP
		   "110": 16,   #P2 JMP (X3)
		   "111": 21}   #P1 JMP

if __name__ == "__main__":
    cpu1 = CPU()
    # load program 1
    cpu1 = load_program(cpu1, "prog1_group_4_p1_bin.txt", "patternD")
    print(cpu1.memory[0:10])
    print("Registers init. to 0 r0=" + str(cpu1.R[0]) + " r1=" + str(cpu1.R[1]) + " r2=" + str(cpu1.R[2]) + " r3=" + str(cpu1.R[3]))

    print("Running Program 1...", end='')
    cpu1 = run_program(cpu1)
    print("Program 1 finished!")
    print("DIC: " + str(cpu1.DIC))
    print("Registers r0=" + str(cpu1.R[0]) + " r1=" + str(cpu1.R[1]) + " r2=" + str(cpu1.R[2]) + " r3=" + str(cpu1.R[3]))
    for m in range(0,6):
        if m == 2:
            print("mem", "[", m, "]=", cpu1.memory[m], "Result")
        else:    
            print("mem", "[", m, "]=", cpu1.memory[m])
    
    # send resulting data memory to file
    output_file = open("p3_group_4_dmem_D.txt", "w")
    for i in range(0,108):
        bin1 = format(cpu1.memory[i], "016b")
        output_file.write(bin1 + "\n")
    
    # load program 2
    cpu2 = load_program(cpu1, "prog1_group_4_p2_bin.txt", "p3_group_4_dmem_D.txt")
    # reset DIC
    cpu2.DIC = 0
    print("Running Program 2...", end='')
    cpu2 = run_program(cpu2)
    print("Program 2 finished!")
    print("DIC: " + str(cpu2.DIC))
    print("Registers r0=" + str(cpu1.R[0]) + " r1=" + str(cpu1.R[1]) + " r2=" + str(cpu1.R[2]) + " r3=" + str(cpu1.R[3]))
    for n in range(0,6):
        if n == 2:
            print("mem", "[", n, "]=", cpu1.memory[n], "Result")
        elif n == 4:
            print("mem", "[", n, "]=", cpu1.memory[n], "Score")
        elif n == 5:
            print("mem", "[", n, "]=", cpu1.memory[n], "Count")
        else:
            print("mem", "[", n, "]=", cpu1.memory[n])
    
    # send resulting data memory to file
    f = open("p3_group_4_dmem_D.txt", 'w') # overwrite previous file
    for i in range(0,108):
        bin2 = format(cpu1.memory[i], "016b")
        f.write(bin2 + "\n")
        
    print("end")

    
    

