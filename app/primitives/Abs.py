# Primitive function: Abs
# Returns the absolute value of a number

__author__="Gonzalo"

from If import If
from Negate import Negate
from Positive import Positive

def Abs (a):
    return If(Positive(a),a,Negate(a))

if __name__ == "__main__":
    print(Abs(1))
    