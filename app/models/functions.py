import traceback
# Author: Drone

import web
from config import db
import string
import sys

from app.models import search as search_model
from app.helpers import utils
#from app.models.solver import Solver, ProblemData
from app.models import solver

def getLatest (offset=0, limit=10):

    """Get the latest functions."""
    has_next = False

    m = list(db.select('function as f, category as c',
        what   = 'f.id, f.name, c.name as category, f.aliases, f.description, f.author, f.datetime_created',
        where  = 'f.categoryId = c.id ',
        order  = 'f.datetime_created desc',
        offset = offset, 
        limit  = limit + 1))

    if len(m) > limit:
        has_next = True
    
    return m[:limit], has_next
    
def getRandom (limit = 3):

    """Get random functions."""
    return db.select('function', 
        what  = 'id, name',
        where = '1=1',
        order = 'rand()', 
        limit = limit)

""" Not used yet """
def getRelated (functionId):

    """Get a similar function."""
    function_aliases = getAliases(functionId)

    m = web.listget(
        db.select('function as f',
            vars  = dict(id=str(functionId), aliases=function_aliases),
            what  = 'f.*',
            where = 'f.id != $id and %s' % web.sqlors("f.aliases = ", function_aliases),
            group = 'f.id having count(f.id) > 1',
            order = 'rand()'), 0, False)
    
    return m and getFunction(m.functionId)

def getFromCategory (categoryId, offset=0, limit=30):
    return db.select('function as f, category as c',
        vars  = dict(categoryId=str(categoryId)),
        what  = 'f.id, f.name, f.aliases, f.description, f.author',
        where = 'f.categoryId = c.id AND c.id = $categoryId',
        order = 'f.datetime_created desc',
        offset = offset,
        limit = limit + 1)

def getCategories ():
    return db.select('category as c',
        what  = 'c.id, c.name',
        order = 'c.name')

def getFromAuthor (author, offset=0, limit=30):
    return db.select('function',
        vars  = dict(author=author),
        what  = 'id, name, aliases, description, author',
        where = 'author = $author',
        order = 'datetime_created desc',
        offset = offset,
        limit = limit + 1)

def getAllFunctions (order_by='name', limit=None, offset=None, **conditions):
    order_by = dict(name='name', author='author',
        date='datetime_created').get(order_by, 'name')
    extras={}
    if limit or offset:
        if not limit:
            limit = 50
        if not offset:
            offset = 0
        extras.update({
            'offset': offset,
            'limit': limit,
        })
    where = ['1=1']
    if 'isPrimitive' in conditions:
        where.append('isPrimitive = $isPrimitive')
    if 'isCorrect' in conditions:
        where.append('isCorrect = $isCorrect')

    has_next = False
    m = list(db.select('function', 
        vars   = conditions,
        what   = '*',
        where  = " AND ".join(where),
        order  = order_by,
        **extras))

    #print("all list"+str(m))
    if len(m) > limit:
        has_next = True
    
    return m[:limit], has_next


def search (query, offset=0, limit=10):
    """ Performs a search of functions by name, author, descripction, aliases, etc """
    return search_model.search(query, offset, limit)


def getFunctionIdByName (name):

    """Get a function id from its name."""
    data = web.listget(
        db.select('function as f',
            vars = dict(name = name),
            what = 'f.id',
            where='f.name = $name'), 0, False)
    if data:
        return data.id
    return None

def getFunction (id):

    """Get a specific function by its id."""
    fn = web.listget(
        db.select('function as f, category as c',
            vars = dict(id=str(id)),
            what = 'f.*, c.name as category',
            where='f.categoryId = c.id AND f.id = $id'), 0, False)
    if fn:
        return fn
    return None

# Create an empty function
def createNew ():
    function = web.Storage()
    function.id=0
    function.name=''
    function.aliases=''
    function.tags=''
    function.categoryId=''
    function.author=''
    function.description=''
    function.rules=''
    function.training=''
    function.isPrimitive=''
    function.isCorrect=''
    function.isCommutative=''
    function.isRecursive=''
    function.source=''
    return function

# Binds the content of the dict to a Storage object
def bind (data=None):
    function = {}
    if data:
        if data.has_key('id'):
            function['id']=data['id']
        function['name']=data['name']
        function['aliases']=data['aliases']
        #function['tags']=data['tags']
        function['categoryId']=data['categoryId']
        function['author']=data['author']
        function['description']=data['description']
        function['rules']=data['rules']
        function['training']=data['training']
        function['isPrimitive']=data['isPrimitive']
        function['isCorrect']=data['isCorrect']
        function['isCommutative']=data['isCommutative']
        function['isRecursive']=data['isRecursive']
        function['source']=data['source']
    return function

# Checks all data in the storage, previously to an insert or update
def checkData (function,isUpdate=False):
    #print function
    if not isUpdate:
        if alreadyExists(function['name']):
            return (False,'That function already exists')
    if len(function['name'])<1:
        return (False,'A function must provide a name')
    if not int(function['categoryId'])>0:
        return (False,'A function must provide a name')
    return (True,'')

def getSource (functionId):
    """Get source of a function by its id."""
    data = web.listget( db.select('function as f', what = 'f.source', vars = dict(id=str(functionId)), where='f.id = $id'), 0, False)
    if data:
        return data.source.split('\n')
    else:
        return []

# Get the module code from a function. Returns none if the function hasn't source yet
def getSourceCode (function, functionNames):

    #print("Training",function.training)
    params = []
    for i in function.training.split('\n'):
        if len(i.strip()):
            #print("A partir "+i)
            if '=' in i:
                paramStr, result = i.strip().split('=')
                #print "Cada uno "+paramStr,result
                if paramStr:
                    params = paramStr.split(',')
                #print("Params ",params)
                break
            else:
                #print("Por aqui")
                params=[]
                break
    paramNames=[]

    for i,p in enumerate(params):
        paramNames.append(chr(i+ord('a')))
    #print("Params names",paramNames)
    source=""
    if len(function.source)!=0:
        #print("hay source!",function.source)
        # Choose the first source
        for node in function.source.split('\n'):
            if ':' in node:
                key, data = node.split(':')
            else:
                key=node
            source=key
            break
    if not source:
        if len(function.rules.strip()):
            source=function.rules.strip()
        elif len(function.training.strip()):
            source=function.training.strip()
        else:
            print("No source for "+function.name)
            return None

    # Construct imports
    imports = "\n".join([ "from %s import %s" % (i,i) for i in functionNames if i!=function.name and i in source] )
    
    # Include math module if needed
    if 'math.' in source:
        imports += "\nimport math"

    content="""# Primitive function: %(name)s
# %(description)s

__author__="%(author)s"

%(imports)s

def %(name)s (%(paramNames)s):
    return %(source)s

if __name__ == "__main__":
    print(%(name)s(%(paramValues)s))
    """ % {"name": function.name.title(),
        "description": "\n# ".join(function.description.split("\n")), "author": function.author,
        "paramNames": ", ".join(paramNames), "source": source,
        "paramValues": ", ".join(params),
        "imports": imports
        }
    return content


# Search primitives suitables for a function
def getPrimitives (id, rules):
    query = rules.strip(",.()[]:;")

    """
    def sqlands(left, lst):
        return left + (' or %s ' % left).join(lst)
    """
    q = [str(w) for w in query.split()]

    where = []
    if q:
        for c in ['name', 'aliases']:
            where.append('FIND_IN_SET(%s,%s)' % (c,web.sqlquote(','.join(q))))
        text_query = '('+' or '.join(where)+')'
    else:
        text_query='1=1'

    params = {'text_query': text_query, 'id': id}

    pList = list(db.query('SELECT f.* FROM function as f WHERE \
        ( (f.isPrimitive=1 AND f.isCorrect=1 AND f.id != %(id)d AND ( %(text_query)s )) OR ( f.id = %(id)d AND f.isRecursive=1 ) )' % params))

    if len(pList)==0:
        pList=getPrimitives(id,'')

    return pList


def getAliases (functionId):
    """Get aliases function by its id."""
    data = web.listget( db.select('function as f', what = 'f.aliases', vars = dict(id=str(functionId)), where='f.id = $id'), 0, False)
    if data:
        return data.aliases.split(',')
    else:
        return []

def getCount ():

    """Get a count of all functions."""
    return int( web.listget( db.query(
        'select count(*) as c from function'
    ),0).c)

def alreadyExists (functionName):
    return web.listget(
        db.select('function', vars = dict(name=functionName), where='name = $name'), 0, False)
    
def add (function):
    message=''
    id=False

    if not function['source'].strip():
            try:
                if function['rules'].strip():
                    function['source']=function['rules'].strip().split('\n')[0]
                else:
                    function['source']=function['training'].strip().split('\n')[0]
                if isinstance(function['source'],list):
                    function['source']=function['source'][0]

            except:
                raise
                pass

    t = db.transaction()
    try:
        id = db.insert('function', **function)

        # Update primitives module
        result, message = updatePrimitivesModule()
    except Exception as e:
        result=False
        message='Error adding function to the database', e
        t.rollback()
    else:
        t.commit()
    return (id,message)

def update (function, clearSource=True):

    message=''
    result=False
    t = db.transaction()
    try:

        #print("Los datos",clearSource,function.isPrimitive,function.isCorrect)
        
        if clearSource and function.isPrimitive=='0' and function.isCorrect=='0':
            print("Deleting source")
            function.source=''
        else:
            if not function.source:
                if function.rules.strip():
                    function.source=function.rules.strip().split('\n')[0]
                else:
                    function.source=function.training.strip().split('\n')[0]

        where='id='+str(function.id)
        #print("A guardar",function)

        db.update('function',where, **function)
        result = True
        # Update primitives module
        if result:
            result,message = updatePrimitivesModule()
    except:
        print(traceback.print_exc())
        result = False
        message='Error updating the function'
        t.rollback()
    else:
        t.commit()
    return (result,message)


def train (function):
    reload(solver)
    primitives = getPrimitives(function.id, function.rules)

    print("Primitives for", function.name, [f.name for f in primitives])
    err_msg=''

    # Determine set of primitives to use
    primitivesData = []
    for i in primitives:
        prData = solver.ProblemData(i)
        primitivesData.append(prData)

    # Set the parameters for the function to solve, primitives to use and old nodes already seen
    fnData = solver.ProblemData(function, primitivesData)

    s = solver.Solver()
    s.setProblem(fnData)
    s.setMaxDepth(8)
    s.setTimeout(90)

    if s.solve()==(None,None):  # with timeout and tolerance
        err_msg="Couldn't begin to train the function"

    try:
        function.source="\n".join([frm + ': ' + str(err) for frm,err in fnData.getSource(1000)])
        minError,bestNode=fnData.getMinError()
        if minError==None:
            err_msg="Couldn't begin to train this function"
        primitivesStr=', '.join([ i.name.strip() for i in primitives ])
        numNodes=fnData.getNumNodes()
    except Exception as e:
        minError = None
        primitivesStr = ''
        bestNode = None
        numNodes = 0
        err_msg='Unexpected error trying to solve'
        traceback.print_exc()

    if minError==0:
        function.isCorrect='1'

    if err_msg=='':
        # Store new aproach in db
        (success, err_msg) = checkData(function,True)
        if success:
            success, err_msg = update(function,False)

    return primitivesStr, bestNode, minError, numNodes, err_msg

def test (function, values):

    reload(solver)
    numNodes = len(values) if values else len([1 for i in function.training.split("\n") if i])
    # Set the parameters for the function to solve, primitives to use and old nodes already seen
    fnData = solver.ProblemData(function)

    err_msg = ''
    totalError = float("inf")
    try:
        source=''
        if len(function.source)!=0:
            for node in function.source.split('\n'):
                if ':' in node:
                    key, data = node.split(':')
                else:
                    key=node
                source=key
                break

        if source:
            totalError = fnData.getError(source)[0]
        else:
            err_msg='No source code for '+ function.name +' yet'
    except:
        err_msg='Error testing function '+ function.name

    return source, numNodes, totalError, err_msg

# Updates the __init__.py file and rewrites primitives only if doesn't exists
# This is called when a function is created or updated
def updatePrimitivesModule ():

    #print("1********")
    functions = getAllFunctions('name', None, None)  # Returns a tuple for pagination!!!
    functionNames = [ f.name.title() for f in functions[0] ]
    #print("1.********")
    imports=[]
    for function in functions[0]:
        #print("1.46")
        if function.isPrimitive==1:
            #print("1.56",function.name)
            if not storePrimitive(function, functionNames):    # Primitives may have not source code in database, so we want to include them but not overwrite its code
                #print("1.75")
                return (False,"Error writing function "+function.name,". Train before mark it as primitive?")
            #print("1.86")
            imports.append(function.name.title())

    #print("2********")
    if imports:
        content="""# Generated file. Do not edit
__author__="drone"

%(imports)s

__all__ = %(functions)s
""" % {"imports": "\n".join(["from "+i+" import "+i for i in imports]),"functions": [i.encode('ascii') for i in imports]}

        finit=open('app/primitives/__init__.py','w')
        #print("2.5********")
        if finit:
            finit.write(content)
            finit.close()
            return (True,"")
    #print("3********")
    return (False,"Error")

# Stores a primitive function as code so will be executable
# If the function doesn't have code or is not primitive
# or there is a problem writting the file, does nothing and returns False
def storePrimitive (function, functionNames):

    if function.isPrimitive==0:
        #print("Not primitive!!!")
        return False

    #print("Before code")
    if not function.source:
        function.source=function.rules
    code=getSourceCode(function,functionNames)
    #print("After code",code)

    if code:
        #print 'app/primitives/'+function.name.title()+'.py'
        ffunc=open('app/primitives/'+function.name.title()+'.py','w')
        if ffunc:
            ffunc.write(code)
            ffunc.close()
        else:
            print("Couldn't open file "+ffunc)
            return False
    else:
        print("No source for ",function.name)
        return False
    return True


