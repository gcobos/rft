# Author: Drone

import web
import mimetypes
from web import http

class GetStream:
    def GET(self): 
        try:
            file_name = web.ctx.path.split('/')[-1]
            web.header('Content-type', mime_type(file_name))
            print "Fichero a abrir: "+ web.ctx.path
            return open(web.ctx.path[1:], 'rb').read()
        except IOError:
            raise web.notfound()
            
def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream' 

class Redirect:
    def GET(self, path): 
        fragments = ''
        if web.input():
            fragments = '?' + http.urlencode(web.input())
        return web.seeother('/' + path + '/' + fragments)