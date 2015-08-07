#!/usr/bin/python3

from copy import copy
from collections import Counter
import sys
from time import time
from heapq import heapify
import itertools


# For each symbol: (isFunction, numParams, isCommutative)
grammar={
	'a': (0,0,0),
	'b': (0,0,0),
	#'c': (0,0,0),
	'Sum': (1,2,1),
	'Mul': (1,2,1),
	#'Max': (1,2,1),
	'Sub': (1,2,0),
	'Half': (1,1,0),
	'Double': (1,1,0),
	'Div': (1,2,0),
}

nodes={}

# Primitives, params of the parent, and the number of funcions to use inside 
def getNodeKey (grammar, level=0, maxLevel=0):

    options = grammar if level<1 else { k: v for k, v in grammar.items() if v[0]}
    chains=set(nodes)
    '''
    # Invert mapping for options
    options_inv = {}
    for k, v in options.items():
        options_inv[v] = options_inv.get(v, [])
        options_inv[v].append(k)
    
    for option, names in options_inv.items():
        print("Row", option, names)
        isFunction, params, isCommutative = option
        if isFunction:
            if isCommutative:
                generator=itertools.combinations_with_replacement(chains,params)
            else:
                generator=itertools.product(chains,repeat=params)
            for j in generator:
                for name in names:
                    formula = "%s(%s)" % (name, ','.join(j))
                    if not formula in chains:
                        nodes[formula]=1
                        yield formula
                    
        else:               	# its a parameter
            for name in names:
                nodes[name]=1
                yield name
            
    '''
    for name in options:
        isFunction, params, isCommutative = options[name]
        if isFunction:
            #print("Using",name)
            if isCommutative:
                generator=itertools.combinations_with_replacement(chains,params)
            else:
                generator=itertools.product(chains,repeat=params)
            for j in generator:
                formula = "%s(%s)" % (name, ','.join(j))
                if not formula in chains:
                    nodes[formula]=1
                    yield formula            
        else:
            nodes[name]=1
            yield name
    
    return


time0=time()
cnt=0
try:
    maxLevel=int(sys.argv[1])
except:
    maxLevel=2

for i in range(1):
    nodes={}
    for level in range(maxLevel):
    
	    print("** Entering level",level)
	
	    for i in getNodeKey(grammar,level=level, maxLevel=maxLevel):
		    #if level==maxLevel-1:
		    #print(i)
		    cnt=cnt+1
t = time()-time0
print("Total,",cnt,"Time ", t, '\nSpeed:', cnt/t/1000)

