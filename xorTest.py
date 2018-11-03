def xor(a, b):
    return a ^ b

if __name__ == "__main__":
    a = -5
    print(str(bin(a)))
    b = 9
    print(str(bin(b)))
    result = xor(a,b)
    print(str(bin(result)))

    a = -5
    print(str(bin(a)))
    b = -11
    print(str(bin(b)))
    result = xor(a,b)
    print(str(bin(result)))
