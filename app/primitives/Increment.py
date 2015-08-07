# Primitive function: Increment
# Gets the next number (+1)

__author__="drone"

from One import One
from Sum import Sum

def Increment (a):
    return Sum(One(),a)

if __name__ == "__main__":
    print(Increment(1 ))
    