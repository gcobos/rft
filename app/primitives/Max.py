# Primitive function: Max
# Returns the biggest number of the list

__author__="Gonzalo"

from If import If
from Lessthan import Lessthan

def Max (a, b):
    return If(Lessthan(b,a),a,b)

if __name__ == "__main__":
    print(Max(1, 2))
    