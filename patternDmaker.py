import sys

outputfile = open("patternD.txt", "w")

def format_z(number):
    return format(number, "016b") + "\n"

outputfile.write(format_z(1007))
outputfile.write(format_z(64))
outputfile.write(format_z(0))
outputfile.write("1111000011110000" + "\n")
outputfile.write(format_z(0))
outputfile.write(format_z(0))
outputfile.write(format_z(0))
outputfile.write(format_z(0))

pattern = "0011001100110011"

for i in range(100):
    pattern = pattern[1:] + pattern[0]
    outputfile.write(pattern + "\n")

outputfile.close()
