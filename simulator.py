import sys
import collections

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
        if len(line) < 1 or line.startswith("#"):
            continue
        cpu.instructions.append(line)

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
            print("ERROR: Parity Bit Error")
            sys.exit()

        if instr[1:8] == "1110 111":
			cpu.R[3] = cpu.R[3] ^ cpu.R[2]
			cnt = bin(cpu.R[3]).count("1")
			cnt = 32 - cnt
			cpu.R[3] = cnt
        elif instr[1:6] == "01100":
            # Add instruction
            Rx = registers[instr[4:6]]
            Ry = registers[instr[6:8]]
            cpu.R[Rx] = cpu.R[Rx] + cpu.R[Ry]
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:6] == "01101":
            # Sub R3 instruction
            Rx = registers[instr[6:8]]
            cpu.R[Rx] = cpu.R[3] - cpu.R[Rx]
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
            Rx = registers[instr[4:5]]
            cpu.R[Rx] = instr[5:8]
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:3] == "11":
            # Branch Equal R0
            Rx = registers[instr[3:5]]
			imm = imm_mux[instr[5:8]]
            if cpu.R[Rx] == cpu.R[0]:
            	cpu.PC = cpu.PC + imm
            cpu.DIC = cpu.DIC + 1
        elif instr[1:4] == "100":
		    # Add immediate 
            Rx = registers[instr[4:6]]
            imm = registers[instr[6:8]]
            cpu.R[Rx] = cpu.R[Rx] + imm
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1
        elif instr[1:4] == "101":
            # Set less than, if so R0 = 1
            Rx = registers[instr[4:6]]
            Ry = registers[instr[6:8]]
            if cpu.R[Rx] < cpu.R[Ry]:
                cpu.R[0] = 1
            else
                cpu.R[0] = 0
            cpu.PC = cpu.PC + 1
            cpu.DIC = cpu.DIC + 1

        else:
            print("Error Unknown command")
            sys.exit()
    return cpu

registers = {"00" : 0,
             "01" : 1,
             "10" : 2,
             "11" : 3}

imm_mux = {"000": -19
		   "001": -12
		   "010": -7
		   "011": -6
		   "100": 2
		   "101": 10
		   "110": 12
		   "111": 18}

if __name__ == "__main__":
    cpu1 = CPU()
    cpu1 = load_program(cpu1, "sample_program_machine.ctz", "sample_memory.txt")
    print(cpu1.memory[0:5])
    cpu1 = run_program(cpu1)
    print(cpu1.R)
    print(cpu1.DIC)
    print(cpu1.memory[0:5])
