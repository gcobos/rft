import Image

# Contract:
# To simulate simple cellular automata.

# Written by Justin Ahmed Siraj Kutlusan, 2006 June


class calculations:
    def __init__(self,which):
	self.against = self.array_maker_2()[which]
	self.check = self.array_maker_1()
	self.array = self.array_maker_3(311)
	self.calculator()
	
    def binary(self, n, size): ## This is the Int -> str(BINARY) converter
	assert n >= 0
	bits = []
	while n:
	    bits.append('01'[n&1])
	    n >>= 1
	bits.reverse()
	result = ''.join(bits) or '0'
	for iteration in range(len(result),size):
	    result = "0" + result
	return result
    
    def array_maker_1(self): # This makes the array that represents the 8 different permutations of 3 cells. Itself, its left and its right.
	return [self.binary(n, 3) for n in range(8)]

    def array_maker_2(self): # This makes the array that represents every single different rule. If for instance the second element in one
    # of these rules is 1, then the corresponding permutation that may be found in the result array (array_maker_3), will be 1 (black).
	return [self.binary(n, 8) for n in range(256)]
    
    def array_maker_3(self, y): # This is the array for all the results. The automaton starts from the middle of the first row
	x = [["0" for x in range((2*y)+1)] for n in range(y)]
	x[0][(2*y+1)/2] = "1"
	return x
    
    def calculator(self): # This cycles over all of the cells, and scans one row at a time, and changes the next row according to the current cell.
	self.buff_result = ["0","0","0"] # This is the current permutation buffer to be checked against the corresponding arrays.
	for i in range(len(self.array)-1):
	    for j in range(1, len(self.array[0])-1):
		self.step1(j,i)
		self.step2(j,i)
		self.step3(j,i)
		y = self.check.index(''.join(self.buff_result))
		self.array[i+1][j] = self.against[y]

# The steps update the result buffer.
    def step1(self, step, y):
	self.buff_result[0] = self.array[y][step-1]

    def step2(self, step, y):
	self.buff_result[1] = self.array[y][step]

    def step3(self, step, y):
	self.buff_result[2] = self.array[y][step+1]

for number in range(256):
    objo = calculations(number)
    x = objo.array
    y = []
    for num,zo in enumerate(x):
	for com,wo in enumerate(zo):
	    x[num][com] = int(wo)
    
    nim = Image.new("1", (623,311))

    for n in x: #converting the array of arrays into a single array so putdata can take it.
	for p in n:
	    y.append(p)
    nim.putdata(y)
    nim.resize((6230/2,3110/2)).save("output" + str(number) + ".png")
    print number

