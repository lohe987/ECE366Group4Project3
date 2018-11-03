import collections

def instr_ld(line):
    # 001 RX RY
    return "001" + registers.get(line[1], "??") + registers.get(line[2], "??")

def instr_str(line):
    # 010 RX RY
    return "010" + registers.get(line[1], "??") + registers.get(line[2], "??")

def instr_addR(line):
    # 01100 RX RY
    return "01100" + registers.get(line[1], "??")

def instr_beqR0(line):
    # 11 RX iii
    return "11" + registers.get(line[1], "??") + jump_target.get(line[2], "???")

def instr_addi(line):
    # 100 RR ii
    return "100" + registers.get(line[1], "??") + convert_imm_value(line[2])[-2:]

def instr_init(line):
    # 000 x iii
    return "000" + registers.get(line[1], "??")[1:2] + convert_imm_value(line[2])[-3:]

def instr_addR2(line):
    # 01110 RR
    return "01110" + registers.get(line[1], "??")

def instr_addR3(line):
    # 01111 RR
    return "01111" + registers.get(line[1], "??")

def instr_sltR0(line):
    # 101 RX RY
    return "101" + registers.get(line[1], "??") + registers.get(line[2], "??")

def instr_haltPC(line):
    # 111 RR RR
    return "1110000"

def instr_scrR3R2(line):
    # 110 11 RR
    return "1110111"

def instr_subR3(line):
    # 01101 RR
    return "01101" + registers.get(line[1], "??")

def add_praity_bit(encoded_line):
    # Adds even parity bit to encoded_line
    # Count the number of zeros and ones in the encoded line
    one_zero_dict = collections.Counter(encoded_line)
    # If number of ones is odd at 1 as the parity bit
    if one_zero_dict["1"] % 2 == 1:
        return "1" + encoded_line
    else:
        return "0" + encoded_line

def convert_imm_value(number):
    if int(number) < 0:
        number = 0xFFFF - int(number[1:]) + 1
    return format(int(number), "016b")

def assemble_file(input_file_name="CTZ_instructions.txt", output_file_name="CTZ_machine_code.txt"):
    # Open files using default args or user provided
    input_file = open(input_file_name, "r")
    output_file = open(output_file_name, "w")

    # For each line in input file process the function
    for line in input_file:
        old_line = line
        comment = ""
        func = "?"
        if line.find("#") > -1:
            comment = line[line.find("#"):]
            comment = comment.strip("\n")

        # Remove comments from code
        line = line.strip()
        if line.startswith("#"):
            output_file.write(line + "\n")
        elif len(line) < 1:
            output_file.write("\n")
        else:
            line = line.replace(",", " ")
            line = line.replace("\n", "")
            line = line.replace("\t", " ")
            line = line.split(" ")
            line = list(filter(None, line))
            func = instructions.get(line[0], "?")
            # Check if function is known if not print error message
            if func == "?":
                output_file.write("UNKNOWN\n")
            else:
                # Encode function then add praity bit
                encoded = add_praity_bit(func(line))
                output_file.write(encoded + " " + comment + "\n")

    input_file.close()
    output_file.close()



instructions = {"ld" : instr_ld,
               "str" : instr_str,
               "addR" : instr_addR,
               "beqR0" : instr_beqR0,
               "addR2" : instr_addR2,
               "init" : instr_init,
               "addR3" : instr_addR3,
               "sltR0" : instr_sltR0,
               "subR3" : instr_subR3,
               "scrR3R2" : instr_scrR3R2,
               "haltPC" : instr_haltPC,
               "addi" : instr_addi}

registers = {"R0" : "00",
             "R1" : "01",
             "R2" : "10",
             "R3" : "11",
             "r0" : "00",
             "r1" : "01",
             "r2" : "10",
             "r3" : "11"}

jump_target = { "finish" : "111",
                "done" : "100",
                "mod" : "010",
                "loop" : "000"}


if __name__ == "__main__":
    input_file_name = "prog1machinecode.txt"
    output_file_name = "prog1_group_4_p1_bin.txt"
    assemble_file(input_file_name, output_file_name)
