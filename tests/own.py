#!/usr/bin/python3

from copy import copy
from collections import Counter
import sys
from time import time

name='average'
params=('a','b')

# For each symbol: (isFunction, numParams, isCommutative)
grammar={
	'b':(0,0,0),
	'a':(0,0,0),
	'sum':(1,2,1),
	'half':(1,1,0),
}

# The only limit is the number of primitive functions used controlled by length param

# F ->N1'('P')'|N2'('P','P')'
# N1 ->'half'
# N2 ->'sum'
# P ->'a'|'b'|F

tables=[ [1,2], [1,2] ]
row=[ 'X' for i in range(len(tables))]

def pScalar (tables,row,tableIndex=None,commutative=False):

	global cache

	indexCache = str(tables)
	if indexCache in cache:
		return cache[indexCache]

	if tableIndex==None:
		tableIndex=len(row)
	
	if tableIndex==1:
		results=[]
		for row[tableIndex-1] in tables[tableIndex-1]:
			results.append(copy(row))
		#print("Opciones:",results)
		return results
	else:
		results=[]
		#print("Empieza el bucle")
		for row[tableIndex-1] in tables[tableIndex-1]:
			if not commutative:
				results.extend(pScalar(tables,row,tableIndex-1))
			else:			
				pack=pScalar(tables,row,tableIndex-1)
				#print("Pack:",pack)
				for i in pack:
					pset=Counter(i)
					#print("Set: ",results)
					#print("Lalal",pset)
					exists=False
					for j in results:
						if pset==Counter(j):
							exists=True
							#print("Existe!",pset,j)
					if not exists:
						results.append(i)
		#print("Termina el bucle con ",results)
		cache[str(tables)]=results	
		return results

"""
def pScalarGen (tables,row,tableIndex=None):

	if tableIndex==None:
		tableIndex=len(row)
	
	if tableIndex==1:
		results=[]
		for row[tableIndex-1] in tables[tableIndex-1]:
			results.append(copy(row))
		yield results
	else:
		results=[]
		for row[tableIndex-1] in tables[tableIndex-1]:
			results+=list(pScalarGen(tables,row,tableIndex-1))[0]
		yield results

print('Generator')
time0=time()
for i in pScalarGen(tables,row):
	pass
	print('PScalar',i)
print('Elapsed generator',time()-time0)
"""
"""
time1=time()
print('Recursive')
for i in pScalar(tables,row,commutative=True):
	print('PScalar',i)
print('Elapsed recursive',time()-time1)
sys.exit()
"""


cache={}


# Primitives, params of the parent, and the number of funcions to use inside 
def getNodeKey (grammar,maxLevel,minLevel=0):

	global cache

	# Retrieve options that fits in the actual level
	options=[ i for i in grammar if grammar[i][0]<= maxLevel and maxLevel>=minLevel]

	#print( "Options en ",maxLevel,": ",options)
	for i in options:
		isFunction,params,isCommutative=grammar[i]
		#print("pilla "+str(i))
		if isFunction:
			menu=list(getNodeKey(grammar, maxLevel-1,minLevel))
			if menu:
				#indexCache = str(menu)
				#if indexCache in cache:
				if not menu:
					scalarResults=cache[indexCache]
					#print("Hit!",)
				else:
					#print("-menu",menu)
					parts=[ menu for i in range(params) ]
					#print("parts:",parts)
					body=[ 'X' for i in range(len(parts))]
					#print("From parts:",parts)
					scalarResults=pScalar(parts,body,commutative=isCommutative)
					#cache[indexCache]=scalarResults
				for j in scalarResults:
					#print("   Chosen: ",j)
					yield i + '(' + ','.join(j) + ')'
		else:               	# its a parameter
			yield i 
	return


time0=time()
cnt=0
maxLevel=int(sys.argv[1])
if len(sys.argv)==3:
	minLevel=int(sys.argv[2])
else:
	minLevel=0
for i in getNodeKey(grammar,maxLevel,minLevel):
	print ("Result: ",i)
	cnt=cnt+1
print("Total:", cnt," en ",time()-time0)

#for i in cache:
#	print("Cache ",i,cache[i])
	