#!/usr/bin/env python
# encoding: utf-8
"""
xmpp.py

Copyright (c) 2010 En-Ran Zhou, Liang-Heng Chen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import logging

from google.appengine.api import users
from google.appengine.ext.webapp import xmpp_handlers

from model.note import Note

def get_current_user(sender):
    logging.debug('sender = %s' % (sender))
    email = sender[:sender.find('/')]
    return users.User(email=email)

class XmppHandler(xmpp_handlers.CommandHandler):
    def reply_query(self, message, query):
        results = []
        for note in query:
            results.append('* %s' % note.title)
        message.reply('%s\ntotal %d results.' % ('\n'.join(results), len(results)))

    def search_command(self, message=None):
        if message is None:
            return
        
        user = get_current_user(message.sender)
        keyword = message.arg

        logging.info('keyword = %s' % (keyword))
        query = Note.all().filter('owner =', user).search(keyword)
        self.reply_query(message, query)

    def list_command(self, message=None, progress_threshold=100):
        if message is None:
            return

        user = get_current_user(message.sender)
        query = Note.all().filter('owner =', user).filter('progress <', progress_threshold).order('progress').order('create_time')
        self.reply_query(message, query)

    def listall_command(self, message=None):
	self.list_command(message, 1000)

    def unhandled_command(self, message=None):
        pass

    def text_message(self, message=None):
        if message is None:
            return
        
        note = Note(
                    owner=get_current_user(message.sender),
                    title=message.body.strip(),
                    priority=0,
                    progress=0,
                )
        note.put()
        message.reply('OK')

