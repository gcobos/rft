# Primitive function: Positive
# Returns 1 if the number is positive (a>=0) or 0 if it's negative

__author__="Gonzalo"

from Lessorequal import Lessorequal
from Zero import Zero

def Positive (a):
    return Lessorequal(Zero(),a)

if __name__ == "__main__":
    print(Positive(12))
    