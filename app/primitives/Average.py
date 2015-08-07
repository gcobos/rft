# Primitive function: Average
# Calculate the average between two values

__author__="drone"

from Half import Half
from Sum import Sum

def Average (a, b):
    return Half(Sum(a,b))

if __name__ == "__main__":
    print(Average(8, 4 ))
    