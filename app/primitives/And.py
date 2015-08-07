# Primitive function: And
# Returns 1 if both "a" and "b" are not 0, else returns 0

__author__="Gonzalo"

from If import If
from One import One

def And (a, b):
    return If(b,If(a,One(),a),b)

if __name__ == "__main__":
    print(And(1, 1))
    