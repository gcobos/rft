# Primitive function: Min
# Chooses the smaller from two numbers

__author__="Gonzalo"

from Greaterthan import Greaterthan
from If import If

def Min (a, b):
    return If(Greaterthan(b,a),a,b)

if __name__ == "__main__":
    print(Min(1, 3))
    