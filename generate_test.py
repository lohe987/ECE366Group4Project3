
# coding: utf-8

# In[25]:


# program to generate some known test arrays
# just mess with p, q, t, and the for loop
# write into a file and use it in the simulator

def make_test(filename, p, q, target):
    output_file = open(filename, "w")
    # init p
    line0 = format(p, "016b")
    # init q
    line1 = format(q, "016b")
    # init r
    line2 = format(0, "016b")
    # init target
    line3 = format(target, "016b")
    # init score, count, ptr1, ptr2
    line4 = format(0, "016b")
    print(line0, line1)
    output_file.write(line0 + "\n" + line1 + "\n" + line2 + "\n" + line3 + "\n" + line4 + "\n" + line4 + "\n" + line4 + "\n" + line4 + "\n")
    # init array values
    for x in range(100):
        if x % 2 == 0:
            output_file.write(format(255, "016b") + "\n")
        else:
            output_file.write(format(21845, "016b") + "\n")
    
    
if __name__ == "__main__":
    print("generating test with p =", 10, "q = 20", "target =", 0)
    make_test("PatternC.txt", 10, 20, 1)
    
    
    

