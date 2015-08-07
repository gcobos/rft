# -*- coding: utf-8 -*-

#import psyco
#psyco.full()

#from Queue import *
#from copy import deepcopy
#import imp
import traceback
import itertools
import heapq
import random
import sys
from gevent import sleep, spawn

sys.path.extend(('.','..','../..','../../..'))

# Takes the environment for evaluation of functions
if sys.modules.get("app.primitives"):
    del sys.modules["app.primitives"]
environment = vars(__import__('app.primitives', {}, {}, ['primitives'], 1))
if '__builtins__' in environment:
    del environment['__builtins__']

# Constants
SOLVED = 0
LIM_TIMEOUT = 1
LIM_THREADS = 2
LIM_MEMORY = 3
NOT_SOLVED = 4


# Doesnt exists in python3 yet :S
"""
def combinations_with_replacement(iterable, r):
    # combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)
"""

# Process and store information of a function to train
class ProblemData:

    def __init__ (self, function, primitives=[]):
        """
        Receives the function and prepare it to the solver
        """
        self.name = function.name.title()
        self.isCommutative = function.isCommutative
        self.isRecursive = function.isRecursive
        self.numParams = 0
        self._primitives = primitives
        self._training = []
        self._nodes = []        # A list with all levels explored. Each level is a heap, with all nodes sorted by its error

        self._parseTraining(function.training)
        #print "Training de "+self._name+" ("+str(self.numParams)+"): "+str(self._training)
        self._parseNodes(function.source)

    def trainingData (self):
        return self.trainingData.__iter__()

    def getNodes (self):
        return self._nodes

    def getNumNodes (self):
        return sum([len(i) for i in self._nodes])

    # Returns a set of candidates to solve the function, and its errors
    def getSource (self, num_rows = 20):
        #for i in itertools.chain(self._nodes):
        #    print("Chain:",i)
        
        if num_rows == 0:
            num_rows=sum([len(i) for i in self._nodes])
        source = []
        try:
            for error, formula in heapq.merge(*self._nodes):
                source.append(formula + ': ' + str(error))
                num_rows-=1
                if num_rows <= 0:
                    break
        except:
            print("Error in getSource", traceback.print_exc())
            pass
        return source

    # Method that evalue the training set given a node key (the candidate formula), the error always should be be positive or zero. "None" means something was wrong
    def getError (self, nodeKey):
        error = None
        if not nodeKey:
            return error
        try:
            error = 0.0
            #print("El training es",self._training)
            for params, result in self._training:
                for i, p in enumerate(params):
                    environment[chr(i + ord('a'))] = p
                error += abs(eval(nodeKey, {}, environment) - result)
                if error:
                    break
            #print("Total error", error)
        except:
            print("Error trying to evaluate ",nodeKey,"with",params)
            print("Result should be",result)
            print traceback.print_exc()
            pass
        return error

    def getMinError (self):
        if len(self._nodes)==0:
            return (None, None)

        for error, formula in heapq.merge(*self._nodes):
            return error, formula
        
        return (None, None)
            
        """
        #print("Todos los niveles",len(self._nodes))
        #print("yyyyy",range(len(self._nodes)))
        minError=(None,None)
        if len(self._nodes):
            try:
                minError=(float("inf"), '') #heapq.heappop(self._nodes[0])
                value=minError
                #heapq.heappush(self._nodes[0],value)
                for i in range(len(self._nodes)-1):
                    try:
                        value=heapq.heappop(self._nodes[i])
                        heapq.heappush(self._nodes[i], value)
                    except:
                        print("Error pushing a new node")
                        pass
                    if value<minError:
                        minError=value
            except:
                print traceback.print_exc()
                raise
        return minError
        """

    def _parseTraining (self, data):
        if data:
            self.numParams = -1
            for i in data.split('\n'):
                if len(i.strip()) and '=' in i:
                    paramStr, result = i.strip().split('=')
                    if len(paramStr.strip()):
                        params = paramStr.split(',')
                        #print("que hace "+self.name,params)
                        try:
                            params = [float(i) for i in params]
                        except:
                            pass
                        if self.numParams == -1 or len(params) < self.numParams:
                            self.numParams = len(params)
                    else:
                        self.numParams = 0
                        params = []
                    try:
                        result=float(result)
                    except:
                        #print("Que es el result",result)
                        pass
                    self._training.append((params, result))
            if self.numParams==-1:
                self.numParams=0

    def _parseNodes (self, data):
        if data:
            self._nodes.insert(0,[])
            latest_formula=''
            for i in data.split('\n'):
                if len(i.strip())>0 and ':' in i:
                    (formula, error) = i.split(':')
                    if formula and float(error)==0:
                        try:
                            if not latest_formula:
                                latest_formula = formula
                                heapq.heappush(self._nodes[0],(float(error),formula))
                            elif formula.count("(") < latest_formula.count("("):
                                heapq.heapreplace(self._nodes[0],(float(error),formula))
                                latest_formula = formula
                        except:
                            pass

class Solver:

    def __init__ (self):
        self._timeout = 0
        self._tolerance = 0
        self._maxDepth = 6
        self._maxThreads = 2
        self._problem = None    # No problem :)
        self._result = NOT_SOLVED

    def setProblem (self, problem):
        self._problem = problem

    def getTolerance (self):
        return self._tolerance

    def setTolerance (self, tolerance):
        """ Sets the tolerance, from 0.0 to 1.0 """
        self._tolerance = tolerance

    def getTimeout (self):
        return self._timeout

    def setTimeout (self, timeout):
        """ Sets the timeout in seconds for the solver. 0 means no timeout """
        self._timeout = timeout

    def getMaxDepth (self):
        return self._maxDepth

    def setMaxDepth (self, depth):
        """ Sets the maximun depth can grow """
        self._maxDepth = depth

    def getMaxThreads (self):
        return self._threads

    def setMaxThreads (self, threads):
        """ Sets the maximum number of threads to be used by the solver """
        self._maxThreads = threads

    def solve (self):
        if self._problem.getNumNodes():
            value = self._problem.getMinError()
            #print("Nodes with least error", value)
            if float(value[0]) == 0:
                return value
            
        if not self._problem._primitives:
            return (None,None)
        try:
            print("With timeout =", self._timeout)
            for i in range(self._maxDepth):
                print('Before expanding level',i)
                spawn(self.expandLevel,i).join(timeout=self._timeout)
                print("Nodes explored",self._problem.getNumNodes(),"in level",i)
                if self._result==SOLVED:
                    break
            if self._problem._nodes:
                value = self._problem.getMinError()
            else:
                value = (None, None)
        except Timeout:
            print("Timeout reached, return the best node")
            value = self._problem.getMinError()
        except:
            print("Something failed")
            raise
        return value

    def expandLevel (self, level=0):
        """ Expands all nodes in a level for a problem, having smaller levels already explored """

        if level >= len(self._problem._nodes):
            self._problem._nodes.insert(level,[])

        #print("In expand level, primitives",self._problem._primitives )

        options=[(i.name,True,i.numParams,i.isCommutative) for i in self._problem._primitives ]   # Functions
        if level == 0:
            options.extend([(chr(ord('a')+i),False,0,False) for i in range(self._problem.numParams)])   # Parameters

        #random.shuffle(options)
        #print( "Using ",options)

        chains=set(itertools.chain(*self._problem._nodes[0:level]))
        
        for name, isFunction, numParams, isCommutative in options:
            sleep(0)    # Gives a chance to yield for the Timeout
            if isFunction:
                if isCommutative:
                    generator = itertools.combinations_with_replacement(chains, numParams)
                else:
                    generator = itertools.product(chains, repeat=numParams)
                for j in generator:
                    formula = name + '(' + ','.join([k[1] for k in j]) + ')'
                    if not formula in chains:
                        error=self._problem.getError(formula)
                        if error==None:
                            print("Error None",formula)
                            continue
                        heapq.heappush(self._problem._nodes[level],(error,formula))
                        if error==0:
                            self._result=SOLVED
                            #return     # We want more alternatives!
                        #yield formula

            else:               	# its a parameter
                error=self._problem.getError(name)
                heapq.heappush(self._problem._nodes[level],(error,name))
                if error==0:
                    self._result=SOLVED
                    return
                #yield name
        return
        
