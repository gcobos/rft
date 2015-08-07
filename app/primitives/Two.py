# Primitive function: Two
# Number 2 constant

__author__="Gonzalo"

from One import One
from Sum import Sum

def Two ():
    return Sum(One(),One())

if __name__ == "__main__":
    print(Two())
    