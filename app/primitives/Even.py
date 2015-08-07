# Primitive function: Even
# Returns 1 if the parameter is an even number, else returns 0

__author__="Gonzalo"

from Module import Module
from Not import Not
from Two import Two

def Even (a):
    return Not(Module(a,Two()))

if __name__ == "__main__":
    print(Even(1 ))
    