#!/usr/bin/env python
# Drone

from gevent import monkey
monkey.patch_all()

import web
import app.controllers


from app.helpers import custom_error

urls = (        
    # front page
    '/',                                    'app.controllers.functions.ListLatest',
    '/page/([0-9]+)/',                      'app.controllers.functions.ListLatest',

    # general list
    '/list/?',                              'app.controllers.functions.ListAll',
    # paging?
    
    # other lists types
    '/list/category/([\-0-9a-zA-Z]+)/?',    'app.controllers.functions.ListFromCategory',
    # paging?
    '/list/author/([\-0-9a-zA-Z]+)/?',      'app.controllers.functions.ListFromAuthor',
    # paging?
    '/list/related/([\-0-9a-zA-Z]+)/?',     'app.controllers.functions.ListRelated',
    # paging?

    # add, view, edit, etc
    '/submit/',                             'app.controllers.functions.Add',
    '/show/([0-9a-zA-Z]+)/?',               'app.controllers.functions.Show',
    '/edit/([0-9a-zA-Z]+)/?',               'app.controllers.functions.Edit',
    '/update/',                             'app.controllers.functions.Edit',
    '/train/([0-9a-zA-Z]+)/?',              'app.controllers.functions.Train',
    '/test/([0-9a-zA-Z]+)/?',               'app.controllers.functions.Test',

    # search browse by function name
    '/search/',                             'app.controllers.search.search',
    '/search/(.*?)/',                       'app.controllers.search.SearchResults',
    # paging?
    
    # static pages
    '/feedback/',                           'app.controllers.feedback.Send',
    '/about/',                              'app.controllers.base.About',
    '/help/',                               'app.controllers.base.Help',
    
    # let lighttpd handle in production
    '/(?:css|img|js|rss)/.+',               'app.controllers.public.Public',
    
    
    # canonicalize /urls to /urls/
    '/(.*[^/])',                            'app.controllers.public.Redirect',

   
    # site admin app
#    '/admin',                              admin.app,    
)

app = web.application(urls, globals())
custom_error.add(app)

if __name__ == "__main__":
    app.run()
