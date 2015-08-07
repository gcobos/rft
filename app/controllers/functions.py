import config
# Author: drone

import web

from app.models import functions
from app.models import rss

from app.helpers import render
from app.helpers import misc
from app.helpers import utils
from config import view, listLimit, projectName

def functionMustExist (meth):
    def new(self, functionName):
        if not functions.getFunctionIdByName(functionName):
            return render.layout('')
        else:
            return meth(self, functionName)
    return new

class ListLatest:
    def GET (self, page = 0):
        #if web.input().has_key('q'):
        #   return web.seeother('/search/?' + utils.url_encode(web.input()))

        latest_functions, has_next = functions.getLatest(offset=page * listLimit)
        return render.layout(
            view.list_functions(latest_functions, has_next, sub_title='Latest Functions')
        )

# Category
class ListCategory:
    def GET(self, page_number):
        page_number = int(page_number)

        latest_functions, has_next = functions.getFromCategory(categoryId=0 ,offset=page_number * listLimit )

        next_page_url = ''
        if has_next:
            next_page_url = '/page/%s/' % (page_number + 1)

        sub_title = 'Latest functions'
        if page_number:
             sub_title += ' - Page %s' % (page_number + 1)

        return render.layout(
            view.list_functions(latest_functions, next_page_url=next_page_url, sub_title=sub_title),
            title = page_number and 'Page %s - Functions' % (page_number + 1) or 'Functions')

class ListAll:
    def GET(self, order_by='name', page_number= 0):
        if not order_by: order_by = ''

        page_number = web.intget(page_number, 0)

        m, has_next = functions.getAllFunctions(order_by, limit=config.listLimit,offset=page_number*config.listLimit)

        next_page_url = ''
        if has_next:
            if not order_by:
                next_page_url = '/list/page/%s/' % (page_number + 1)
            else:
                next_page_url = '/list/by-%s/%s/' % (order_by, page_number + 1)
        sub_title = 'Page %s' % (page_number + 1)

        return render.layout(
            view.all_functions(m, functions.getCount(), order_by, next_page_url, sub_title=sub_title),
            title = ('All functions - %s - '+projectName) % sub_title,
            mode = 'modeAllModules')

class Add:
    def GET (self, functionId=0):
        categories = functions.getCategories()
        if functionId:
            function = functions.getFunction(FunctionId)
        else :
            function = functions.createNew()

        return render.layout(view.submit_function(function, categories, action='submit'),
            title='Submit function - ' + projectName)

    def POST (self):
        data = web.input( isPrimitive='0', isCorrect='0', isCommutative='0', isRecursive='0', _unicode=False)

        function = functions.bind(data)
        print "Lalal"+ str(function)
        (success, err_msg) = functions.checkData(function)
        if success:
            success, err_msg = functions.add(function)
            #rss.update_rss()

        return render.layout(view.submitted_form(success, type='submit', err_msg=err_msg),
            title='Submit function - ' + projectName)

class Edit:
    @functionMustExist
    def GET (self, functionName):
        functionId = functions.getFunctionIdByName(functionName)
        function = functions.getFunction(functionId)
        print function
        categories = functions.getCategories()

        return render.layout(view.submit_function(function, categories, action='update'),
            title='Edit function - ' + projectName)

    def POST (self):
        function = web.input( isPrimitive='0', isCorrect='0', isCommutative='0', isRecursive='0', _unicode=False)

        (success, err_msg) = functions.checkData(function,True)
        if success:
            #print "Updating2 "+ str(function)
            success, err_msg = functions.update(function)

            if success:
                web.seeother('/show/'+function.name)


        return render.layout(view.submitted_form(success, type='submit', err_msg=err_msg),
            title='Submit function - ' + projectName)


class Show:
    @functionMustExist
    def GET(self, functionName):
        functionId = functions.getFunctionIdByName(functionName)
        function = functions.getFunction(functionId)
        #print "La function ",function
        related_functions = functions.getRelated(functionId)

        """
        source=function.source.split("\n")
        print("Source",source)
        if len(source):
            if ':' in source[0]:
                source, error = source[0].split(':')
            function.source=source
        """
        
        return render.layout(view.show_function(function, related_functions, misc.get_pub_id()),
            title=function.name + ' - ' + projectName)




class Train:
    """ 1) Extracts training data and the last source from the function
        2) Number of parameters and training information is stored in a object functionData
        3) Retrieves the list of functions availables as primitives, as tools for search the solution, each one with a training
        4) Number of parameters and

    """
    @functionMustExist
    def GET (self, functionName):
        functionId = functions.getFunctionIdByName(functionName)
        function = functions.getFunction(functionId)
        del(function.category)

        (primitivesStr, bestNode, minError, numNodes, err_msg) = functions.train(function)

        return render.layout(view.train_function(function, primitivesStr, bestNode, minError, numNodes, err_msg ),
            title='Training '+functionName+' - ' + projectName)

class Test:
    """ 1) Extracts training data and the last source from the function
        2) Number of parameters and training information is stored in a object functionData
        3) Retrieves the list of functions availables as primitives, as tools for search the solution, each one with a training
        4) Number of parameters and

    """
    @functionMustExist
    def GET (self, functionName):
        functionId = functions.getFunctionIdByName(functionName)
        function = functions.getFunction(functionId)
        del(function.category)
        values = []
        (source, numNodes, totalError, err_msg) = functions.test(function, values)

        return render.layout(view.test_function(function, source, numNodes, totalError, err_msg ),
            title='Testing '+functionName+' - ' + projectName)

