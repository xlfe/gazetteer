import datetime
from google.appengine.ext import db
from google.appengine.tools import bulkloader
import models


class SearchLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'searchindex',
                                   [('token', str),
                                    ('scores', db.Text),
                                   ])

loaders = [SearchLoader]