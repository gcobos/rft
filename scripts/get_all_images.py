import web
db = web.database(dbn='mysql', db='googlemodules', user='ale', passwd='3babes')

for url in db.select('function', what='screenshot'):
    print 'http://www.googlemodules.com/image/screenshot'
