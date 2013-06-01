#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
import re
import datetime
from collections import defaultdict
from google.appengine.ext import ndb

class EmploymentNotice(ndb.Model):
   salary = ndb.StringProperty()
   NoticeNumber = ndb.IntegerProperty()
   classification = ndb.StringProperty()
   PSGazette = ndb.StringProperty()
   text = ndb.TextProperty()
   documentation = ndb.TextProperty()
   toapply = ndb.TextProperty()
   ending = ndb.TextProperty()
   closing_date = ndb.DateProperty()
   contact = ndb.StringProperty()
   location = ndb.StringProperty()
   jobtitle = ndb.StringProperty()
   department = ndb.StringProperty()
   Page = ndb.StringProperty()
   jobtype = ndb.StringProperty()


class searchindex(ndb.Model):
    token = ndb.StringProperty(indexed=True,required=True)
    scores = ndb.TextProperty(indexed=False,required=True)


def ngrams(tokens, MIN_N=3, MAX_N=3):
    n_tokens = len(tokens)
    for i in xrange(n_tokens):
        for j in xrange(i+MIN_N, min(n_tokens, i+MAX_N)+1):
            yield tokens[i:j]

def calc_intersect(results,number=10):

    intersect = defaultdict(int)
    for r in results:

        if r is None:
            continue

        scores = r.scores.split('],')

        for score in scores:

            nn,s = score[2:].split(',')
            nn= int(nn)
            s=float(s.replace(']',''))

            intersect[nn] += 1


    return sorted(intersect,key=lambda k:intersect[k],reverse=False)[:number]







class MainHandler(webapp2.RequestHandler):
    def get(self):


        q = self.request.get('q')
        term_count = defaultdict(int)
        terms = []


        for w in re.split('\W',re.sub('[^A-Za-z]+',' ',q)):
            if len(w) > 2:
                terms.extend([t for t in ngrams(w.lower())])



        for t in terms:
            term_count[t] += 1

        later = []
        for t in term_count:
            later.append(searchindex.query().filter(searchindex.token==t).get_async())

        results = []
        for l in later:
            results.append(l.get_result())


        docs = calc_intersect(results)
        later = []
        for d in docs:
            later.append(EmploymentNotice.query().filter(EmploymentNotice.NoticeNumber==d).get_async())

        results = []
        for l in later:
            results.append(l.get_result().to_dict())




        self.response.write(json.dumps(results,indent=1))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
