#!/usr/bin/python2.7

#import psyco
from copy import copy
from collections import Counter
import sys
from time import time
from heapq import heapify
import itertools

#psyco.full()


# For each symbol: (isFunction, numParams, isCommutative)
grammar={
	'a':(0,0,0),
	'b':(0,0,0),
	'Sum':(1,2,1),
	#'Half':(1,1,0),
	#'div':(1,2,0),
}

# The only limit is the number of primitive functions used controlled by length param

# F ->N1'('P')'|N2'('P','P')'
# N1 ->'half'
# N2 ->'sum'
# P ->'a'|'b'|F

tables=[ [1,2], [1,2] ]
row=[ 'X' for i in range(len(tables))]

"""
print("Product")
for p in itertools.product(['a','b','c','d'],repeat=2):
	print(p)
"""
"""
print("Permutations")
for p in itertools.permutations(['a','b','c','d'],2):
	print(p)
"""
"""
print("Permutations without repetition?")
for p in itertools.permutations(['a','b','c','d','e'],2):
	if p[0] < p[-1]:
		print(p)
"""
"""
print("Combinations")
for p in itertools.combinations(['a','b','c','d','e'],2):
	print(p)
"""
"""
print("Combinations with replacement")
for p in itertools.combinations_with_replacement(['a','b','c','d'],3):
	print(p)
"""
#sys.exit()

# Con bucles!!!
def pScalar (tables, commutative=False):
	case=len(tables)
	results=[]

	if case==0:
		return results
	elif case==1:
		return tables
	elif case==2:
		for i in tables[0]:
			for j in tables[1]:
				results.append((i,j))	
	elif case==3:
		for i in tables[0]:
			for j in tables[1]:
				for k in tables[2]:
					results.append((i,j,k))
	elif case==4:
		for i in tables[0]:
			for j in tables[1]:
				for k in tables[2]:
					for l in tables[3]:
						results.append((i,j,k,l))
	elif case==5:
		for i in tables[0]:
			for j in tables[1]:
				for k in tables[2]:
					for l in tables[3]:
						for m in tables[4]:
							results.append((i,j,k,l,m))
	elif case==6:
		for i in tables[0]:
			for j in tables[1]:
				for k in tables[2]:
					for l in tables[3]:
						for m in tables[4]:
							for n in tables[5]:
								results.append((i,j,k,l,m,n))
	return results		

def pScalarOld (tables,row,tableIndex=None,commutative=False):

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

"""
Planning: Las formulas te generan, nivel a nivel
En el nivel 0 estan los parametros

En el nivel 1, las primeras formulas. Para generar sum se parte de los nodos en el nivel anterior, que son [a, b]
Con eso, se genera el producto escalar para los dos parametros, y ya tengo todos los nuevos nodos, que se anyaden a la cola del nivel 1
Asi que para el nivel 1, resultan:
sum(a,a)
sum(a,b)
sum(b,b)
half(a)
half(b)

En el nivel 2, se vuelven a tener las mismas opciones para las funciones, pero muchas mas para los parametros. Ademas, el nivel 2 admite los parametros del nivel 1 en suma



"""

nodes=[]

# Primitives, params of the parent, and the number of funcions to use inside 
def getNodeKey (grammar, level=0):

    global nodes

    if len(nodes)>=level-1:
        #print('Adding level ',level)
        nodes.insert(level,[])

    options = grammar
    #if level==0:
    #	options=[ i for i in grammar if grammar[i][0]==0 ]   # Parameters
    #else:
    #	options=[ i for i in grammar if grammar[i][0]==1 ]	# Functions

    #print("Nodes",nodes)

    print("Options en ",level,": ",options)
    for i in options:
        isFunction,params,isCommutative=grammar[i]
        print("pilla "+str(i))
        if isFunction:
            if isCommutative:
                generator=itertools.combinations_with_replacement(itertools.chain(*nodes[level-1:level]),params)
            else:
                generator=itertools.product(itertools.chain(*nodes[level-1:level]),repeat=params)
            for j in generator:
                    print('From generator',j)
                    nodes[level].append(i + '(' + ','.join(j) + ')')
                    yield i + '(' + ','.join(j) + ')'

        else:               	# its a parameter
            nodes[level].append(i)
            yield i
    return


time0=time()
cnt=0
try:
    maxLevel=int(sys.argv[1])
except:
    maxLevel=3

nodes=[]
for level in range(maxLevel):
    
	print("** Entrando en el nivel",level)
	
	for i in getNodeKey(grammar,level=level):
		#print (i)
		cnt=cnt+1
print("Total,",cnt,"Time ",time()-time0)

