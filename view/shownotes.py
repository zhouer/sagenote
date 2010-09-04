#!/usr/bin/env python
# encoding: utf-8
import os

from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import db, webapp
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

class RpcHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            # FIXME:
            return

        pos = self.request.uri.find('?')
        params = {}
        if pos != -1:
            tmp = self.request.uri[pos + 1:]
            tmp = tmp.split('&')
            for p in [s.split('=') for s in tmp]:
                params[p[0]] = p[1]

        if not params.has_key('action'):
            params['action'] = 'read'

        if params['action'] == 'create':
            note = Note(title=params.get('title', 'No title'),
                        priority=int(params.get('priority', 0)),
                        progress=int(params.get('progress', 0)))
            note.put()
            self.redirect('/')

        elif params['action'] == 'read':
            query = Note.all().filter('owner =', user)

            sort_method = params.get('sort', 'create_time')
            if sort_method == 'create_time':
                query.order('create_time')
            elif sort_method == 'priority':
                query.order('priority')

            notes = {'notes': []}
            for note in query:
                d = { 'key': str(note.key()),
                      'create_time': str(note.create_time),
                      'title': note.title,
                      'priority': note.priority,
                      'progress': note.progress,
                    }
                notes['notes'].append(d)

            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(simplejson.dumps(notes))

        elif params['action'] == 'update':
            if not params.has_key('key'):
                # FIXME:
                return

            key = db.Key(params['key'])
            if not key:
                # FIXME:
                return

            note = db.get(key)
            note.title = params.get('title', note.title)
            note.priority = int(params.get('priority', note.priority))
            note.progress = int(params.get('progress', note.progress))
            note.put()
            self.redirect('/')

        elif params['action'] == 'delete':
            db.get(db.Key(params['key'])).delete()
            self.redirect('/')
