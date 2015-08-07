# -*- coding: utf-8 -*-

#import psyco
#psyco.full()

import traceback
import itertools
import random
import sys
import math
from gevent import sleep, Timeout

sys.path.extend(('.','..','../..','../../..'))

# Takes the environment for evaluation of functions
if sys.modules.get("app.primitives"):
    del sys.modules["app.primitives"]
environment = vars(__import__('app.primitives', {}, {}, ['primitives'], 1))
environment['math']=globals()['math']
if '__builtins__' in environment:
    del environment['__builtins__']

# Constants
SOLVED = 0
LIM_TIMEOUT = 1
LIM_THREADS = 2
LIM_MEMORY = 3
NOT_SOLVED = 4

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
        self._nodes = {}

        self._parseTraining(function.training)
        #print "Training de "+self._name+" ("+str(self.numParams)+"): "+str(self._training)
        self._parseNodes(function.source)

    def trainingData (self):
        return self.trainingData.__iter__()

    def getNodes (self):
        return self._nodes

    def getNumNodes (self):
        return len(self._nodes)

    # Returns a set of candidates to solve the function, and its errors
    def getSource (self, num_rows = 100):
        source = []
        try:
            source = sorted([(k,round(v[0],6)) for k, v in self._nodes.items() if not math.isnan(v[0])], 
                key=lambda i: i[1]*100000000 + i[0].count("(") + len(i[0]))
        except:
            print("Error in getSource", traceback.print_exc())
            pass
        return source[:num_rows]

    # Method that evalue the training set given a node key (the candidate formula), the error always should be be positive or zero. "None" means something was wrong
    def getError (self, func, args = None):
        error = None
        results = []
        if not func:
            return error, results
        try:
            error = 0.0
            if not args:
                #print("No args for", func)
                for params, expected in self._training:
                    for i, p in enumerate(params):
                        environment[chr(i + ord('a'))] = float(p)
                    if args!=None:
                        result=eval(func+'()', {}, environment)
                    else:
                        result=eval(func, {}, environment)
                    if math.isinf(result):
                        results.append("float('%s')" % repr(result))
                    else:
                        results.append(str(result))
                    error += abs(result - expected)
            else:
                for row in zip(self._training, zip(*args)):
                    result=eval("%s(%s)" % (func, ','.join(row[1])), {}, environment)
                    #print("Result for row", row, "is", result)
                    if math.isinf(result):
                        results.append("float('%s')" % repr(result))
                    else:
                        results.append(str(result))
                    error += abs(result - row[0][1])
                    
            #print("Total error", error)
        except:
            print("Error trying to evaluate ",func,"with",args)
            #print("Result should be", expected)
            print traceback.print_exc()
            error = None
            
        if not results:
            error = float("inf")
        return error, results

    def getMinError (self):
        if self._nodes:
            formula, error = self.getSource(1)[0]
            return error, formula
        else:
            return (None, None)
            
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
            latest_formula=''
            for i in data.split('\n'):
                if len(i.strip())>0 and ':' in i:
                    (formula, error) = i.split(':')
                    if formula and float(error)==0:
                        try:
                            if not latest_formula:
                                latest_formula = formula
                            if formula.count("(") <= latest_formula.count("("):
                                self._nodes[formula] = (float(error), None)
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
            with Timeout(self._timeout):
                for i in range(self._maxDepth):
                    print('Before expanding level',i)
                    self.expandLevel(i)
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

        options=[(i.name,True,i.numParams,int(i.isCommutative)) for i in self._problem._primitives ]   # Functions
        if level == 0:
            options.extend([(chr(ord('a')+i),False,0,0) for i in range(self._problem.numParams)])   # Parameters

        #random.shuffle(options)
        #print( "Using ",options)

        chains=set(self._problem._nodes)
        #print("Chains", chains)
        
        for name, isFunction, numParams, isCommutative in options:
            #sleep(0)    # Gives a chance to yield for the Timeout
            if isFunction:
                if isCommutative:
                    generator = itertools.combinations_with_replacement(chains, numParams)
                else:
                    generator = itertools.product(chains, repeat=numParams)
                for j in generator:
                    formula = "%s(%s)" % (name, ','.join(j))
                    if not formula in chains:
                        sleep(0)    # Gives a chance to yield for the Timeout                        
                        error, results=self._problem.getError(name, tuple(self._problem._nodes[k][1] for k in j))
                        self._problem._nodes[formula] = (error, results)
                        if error==0:
                    	    #sleep(0)	# yields
                            print("Found a solution!",formula)
                            self._result=SOLVED
                            #return     # We want more alternatives!
                        #yield formula

            else:               	# its a parameter
                error, results=self._problem.getError(name)
                self._problem._nodes[name] = (error, results)
                if error==0:
                    self._result=SOLVED
                    return
                #yield name
        return
        
