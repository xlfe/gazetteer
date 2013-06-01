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
   salary = ndb.IntegerProperty(indexed=True)
   NoticeNumber = ndb.IntegerProperty()
   classification = ndb.StringProperty()
   PSGazette = ndb.StringProperty()
   date_gazetted = ndb.DateTimeProperty(indexed=True)
   text = ndb.TextProperty()
   documentation = ndb.TextProperty()
   toapply = ndb.TextProperty()
   ending = ndb.TextProperty()
   closing_date = ndb.DateTimeProperty()
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

def calc_intersect(terms,number=15):

    intersect = defaultdict(int)

    for term in terms:

        if term is None:
            continue

        for doc_details in term.scores.split('],'):

            notice,score = doc_details[2:].split(',')
            notice= int(notice)
            score = float(score.replace(']',''))

            intersect[notice] += 1#score


    return sorted(intersect,key=lambda k:intersect[k],reverse=True)[:number]

#hybrid of count and score based on number of terms...





class MainHandler(webapp2.RequestHandler):
    def get(self):


        #for i in range(100):
        #    query = EmploymentNotice.query().fetch(500,keys_only=True)
        #    ndb.delete_multi(query)
        #return



        q = self.request.get('q')
        term_count = defaultdict(int)
        terms = []

        for w in re.split('\W',re.sub('[^a-z]+',' ',q.lower())):
            if len(w) > 3:
                terms.append(w)

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
            results.append(l.get_result())




        self.response.write(json.dumps([r.to_dict() for r in results if r is not None],indent=1))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
