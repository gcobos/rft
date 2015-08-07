# Primitive function: Cube
# Returns the cube of a number =  N^3

__author__="Gonzalo"

from Multiply import Multiply

def Cube (a):
    return Multiply(Multiply(a,a),a)

if __name__ == "__main__":
    print(Cube(1 ))
    