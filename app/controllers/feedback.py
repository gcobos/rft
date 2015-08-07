# Author: Alex Ksikes 
import web

#from app.models import functions

from app.helpers import render
from config import view, projectName
        
class send:
    def GET(self):
        return render.layout(
            view.feedback(), title='Feedback - ' + projectName)
    
    def POST(self):
        i = web.input()
        success = send_feedback(i.author_email, i.subject, i.comment)
        
        return render.layout(
            view.submitted_form(success, type='feedback'), 
            title='Feedback - '+ projectName)

def send_feedback(_from, subject, message):
    to = ['gcobos@gmail.com']
    
    success = False
    if _from and message:
        web.sendmail(_from, ','.join(to), projectName + ': ' + subject, message)
        success = True
    return success
