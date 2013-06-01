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
import datetime
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


class MainHandler(webapp2.RequestHandler):
    def get(self):

        en = EmploymentNotice()
        en.salary = 'some'
        en.NoticeNumber= 192372832
        en.classification = 'APS6'
        en.PSGazette = 'PS4'
        en.text ='somthig'
        en.documentation ='somthig'
        en.toapply ='somthig'
        en.ending ='somthig'
        en.closing_date = datetime.date(year=2012,month=02,day=03)
        en.contact = 'none'
        en.location = 'canberra'
        en.jobtitle = 'manager'
        en.department = 'dbcde'
        en.page = '233'
        en.jobtype = 'fulltimetext'
        en.put()

        #for i in range(10):
        #    query = searchindex.query().fetch(500,keys_only=True)
        #    ndb.delete_multi(query)

        #si = searchindex()
        #si.token = 'abc'
        #si.scores = 'hmm'
        #si.put()

        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
