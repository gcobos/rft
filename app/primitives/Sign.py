# Primitive function: Sign
# Returns 1 if "a" is positive, 0 if "a" is exactly 0, and -1 if "a" is negative

__author__="Gonzalo"

from If import If
from Negate import Negate
from One import One
from Positive import Positive

def Sign (a):
    return If(Positive(a),If(a,One(),a),Negate(One()))

if __name__ == "__main__":
    print(Sign(154))
    