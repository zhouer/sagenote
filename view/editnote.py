#!/usr/bin/env python
# encoding: utf-8
import os

from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required

import settings
from model.note import Note

class DisplayHandler(webapp.RequestHandler):
    @login_required
    def get(self):
        user = users.get_current_user()
        key = self.request.uri.split('/')[-1]
        note = db.get(db.Key(key))
        if note.owner != user:
            # FIXME:
            return

        param = { 'key': key,
                  'title': note.title if note.title else '',
                  'content': note.content if note.content else '',
                }

        path = os.path.join(settings.TEMPLATE_PATH, 'editnote.html')
        out = template.render(path, param)
        self.response.out.write(out)
