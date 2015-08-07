# Primitive function: Plus2
# A number plus 2

__author__="Gonzalo"

from Double import Double
from One import One
from Sum import Sum

def Plus2 (a):
    return Sum(a,Double(One()))

if __name__ == "__main__":
    print(Plus2(-1 ))
    