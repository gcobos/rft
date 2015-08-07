# Author: Drone

import web

from app.models import functions

from app.helpers import utils
from app.helpers import render
from app.helpers import misc

from config import view, projectName

class About:
    def GET(self):
        return render.layout(
            view.about(misc.getCredits()), title='About - ' + projectName)
    
class Help:
    def GET(self):
        return render.layout(view.help(functions.getCount()), title='FAQ - ' + projectName)
