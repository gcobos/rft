# Primitive function: Module
# Module of a division

__author__="drone"



def Module (a, b):
    return a % b if b else a

if __name__ == "__main__":
    print(Module(3, 0))
    