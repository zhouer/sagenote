#!/usr/bin/env python
# encoding: utf-8

from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import db, webapp

from model.note import Note

class RpcHandler(webapp.RequestHandler):
    def readall(self, user):
        query = Note.all().filter('owner =', user)

        hide_complete = self.request.get('hide_complete', 'false').upper() == 'TRUE'

        sort_method = self.request.get('sort', 'create_time')
        if sort_method in ('create_time', 'due_time',
                           'title', 'priority', 'progress'):
            query.order(sort_method)

        notes = {'notes': []}
        for note in query:
            if note.progress < 100 or not hide_complete:
                d = { 'key': str(note.key()),
                      'create_time': str(note.create_time),
                      'title': note.title,
                      'priority': note.priority,
                      'progress': note.progress,
                      'due_time': str(note.due_time),
                    }
                notes['notes'].append(d)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps(notes))

    def readpost(self, user, key):
        note = db.get(db.Key(self.request.get('key', None)))
        if note.owner != user:
            # FIXME:
            return

        resp = { 'owner': note.owner.nickname(),
                 'create_time': str(note.create_time),
                 'title': note.title,
                 'content': note.content,
                 'keywords': note.keywords,
                 'priority': note.priority,
                 'progress': note.progress,
                 'complete_time': str(note.complete_time),
                 'due_time': str(note.due_time),
               }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps(resp))

    def get(self):
        user = users.get_current_user()
        if not user:
            # FIXME:
            return

        action = self.request.get('action', 'read')

        if action == 'read':
            key = self.request.get('key', None)
            if key:
                self.readpost(user, key)
            else:
                self.readall(user)

        elif action == 'delete':
            db.get(db.Key(self.request.get('key', None))).delete()
            self.redirect('/')

    def post(self):
        user = users.get_current_user()
        if not user:
            # FIXME:
            return

        action = self.request.get('action', 'read')
        if action == 'create':
            note = Note(title=self.request.get('title', 'No title'),
                        priority=int(self.request.get('priority', 0)),
                        progress=int(self.request.get('progress', 0)))
            note.put()
            self.redirect('/')

        elif action == 'update':
            note = db.get(db.Key(self.request.get('key', None)))
            if not note:
                # FIXME:
                return

            title = self.request.get('title', None)
            content = self.request.get('content', None)
            priority = self.request.get('priority', None)
            progress = self.request.get('progress', None)
            if title is not None:
                note.title = title
            if content is not None:
                note.content = content
            if priority is not None:
                note.priority = int(priority)
            if progress is not None:
                note.progress = int(progress)

            note.put()
            self.redirect('/')
