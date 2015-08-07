# Primitive function: Quadruple
# Returns four times a number

__author__="Gonzalo"

from Double import Double

def Quadruple (a):
    return Double(Double(a))

if __name__ == "__main__":
    print(Quadruple(1))
    