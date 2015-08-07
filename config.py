# Author: Drone

import web

from app.helpers import utils
from app.helpers import formatting

projectName = 'Remote Function Trainer'

listLimit = 40

# connect to database
db = web.database(dbn='mysql', db='rft', user='root', passwd='1234')
t = db.transaction()
#t.commit()

# in development debug error messages and reloader
web.config.debug = False

# in develpment template caching is set to false
cache = False

# template global functions
globals = utils.get_all_functions(formatting)

# set global base template
view = web.template.render('app/views', cache=cache, globals=globals)

# in production the internal errors are emailed to us
web.config.email_errors = ''