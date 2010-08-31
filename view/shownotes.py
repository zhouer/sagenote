import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from model.note import Note

class DisplayHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            param = { 'notes' :Note.all().filter('owner =', user) }
            path = os.path.join(os.path.dirname(__file__), 'shownotes.html')
            out = template.render(path, param)
            self.response.out.write(out)
        else:
            self.redirect(users.create_login_url(self.request.uri))
