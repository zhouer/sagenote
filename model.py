#!/usr/bin/env python
# encoding: utf-8
"""
model.py

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
import random
import re
import string

from google.appengine.ext import db, search

class Note(search.SearchableModel):
    # mandatory
    owner = db.UserProperty(required=True, auto_current_user_add=True)
    create_time = db.DateTimeProperty(required=True, auto_now_add=True)
    title = db.StringProperty(required=True)

    # optional
    content = db.TextProperty()
    keywords = db.StringListProperty()
    priority = db.IntegerProperty()
    progress = db.IntegerProperty()
    complete_time = db.DateTimeProperty()
    due_time = db.DateTimeProperty()

    def build_keyword(self):
        logging.debug('build_keyword')
        sre = re.match(r'^\[(.*?)\]', self.title.strip())
        if sre is not None:
            keywords = sre.group(1).split(',')
            self.keywords = filter(lambda k: k, 
                    map(lambda k: ' '.join(string.split(k)), keywords))
            logging.info('keywords: %s' % ', '.join(self.keywords))

    def put(self):
        self.build_keyword()
        search.SearchableModel.put(self)
    
