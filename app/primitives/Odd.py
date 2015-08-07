# Primitive function: Odd
# Returns 1 if the number is odd

__author__="Gonzalo"

from Even import Even
from Not import Not

def Odd (a):
    return Not(Even(a))

if __name__ == "__main__":
    print(Odd(-3))
    