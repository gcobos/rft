# Primitive function: If
# Depending on the first parameter, returns the second one or the third

__author__="drone"



def If (a, b, c):
    return b if a else c

if __name__ == "__main__":
    print(If(1, 2, 3))
    