import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import settings
from model.note import Note

class DisplayHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            query = Note.all().filter('owner =', user).order('create_time')
            param = { 'notes': query }
            path = os.path.join(settings.TEMPLATE_PATH, 'shownotes.html')
            out = template.render(path, param)
            self.response.out.write(out)
        else:
            self.redirect(users.create_login_url(self.request.uri))
