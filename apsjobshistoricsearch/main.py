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
import random
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
   #closing_date = ndb.DateTimeProperty()
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

def calc_intersect(terms,number=500):

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

        if self.request.get('home',True) is True:

            return self.redirect('/index.html');



        q = self.request.get('q',None)
        json = self.request.get('json',None)
        if json is not None:
            json = True
        else:
            json = False

        limit = int(self.request.get('limit','100'))
        try:
            if limit > 500 or limit < 0:
                limit = 500
        except:
            limit = 500

        later = []

        if q is not None:
            term_count = defaultdict(int)
            terms = []

            for w in re.split('\W',re.sub('[^a-z]+',' ',q.lower())):
                if len(w) > 3:
                    terms.append(w)

            for t in terms:
                term_count[t] += 1

            later = []
            #maximum of 15 terms...
            i=0
            for t in sorted(term_count,key=lambda k:term_count[k],reverse=True):
                i+=1
                if i>15:
                    break
                later.append(searchindex.query().filter(searchindex.token==t).get_async())

            results = []
            for l in later:
                results.append(l.get_result())

            docs = calc_intersect(results,limit)
            later = []
            for d in docs:
                later.append(EmploymentNotice.query().filter(EmploymentNotice.NoticeNumber==d).get_async())

        else:
            #get 100 random documents...

            #count       76662.000000
            #mean     10477858.150492
            #std         71319.544862
            #min      10350210.000000
            #25%      10416019.250000
            #50%      10478853.000000
            #75%      10537770.750000
            #max      10606766.000000
            #dtype: float64

            later = []
            for i in range(150):
                start = random.randint(10350210,10606000)
                later.append(EmploymentNotice.query()\
                    .filter(EmploymentNotice.NoticeNumber==start)\
                    .get_async())

        results = []
        for l in later:
            results.append(l.get_result())

        responses = []

        included_fields = ['salary','NoticeNumber','classification','PSGazette',
                           'ending','location','jobtitle','jobtype','department',]

        for r in results:
            if r is None:
                continue

            dd = {}
            rd = r.to_dict()
            for f in included_fields:
#                if f not in rd:
 #                   continue
                if len(str(rd[f])) > 4096:
                    dd[f] = rd[f][:4096] + '....'
                else:
                    dd[f] = rd[f]

            dd['gazetted'] = str(r.date_gazetted)
            responses.append(dd)

        if json:
            self.response.write(json.dumps(responses,indent=1))
        else:
            #csv

            header = []
            for d in responses[0]:
                header.append(d)

            self.response.write(','.join(h for h in header))
            self.response.write('\n')

            for d in responses:
                self.response.write(','.join(str(d[h]) for h in header))
                self.response.write('\n')



app = webapp2.WSGIApplication([
    ('/api/.*', MainHandler)
], debug=True)
