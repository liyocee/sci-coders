__author__ = 'erico'

from google.appengine.ext import ndb
from models.custom_user import CustomUser
import logging

#Item model
#
#  - title
#  - description
#  - price
#  - creation time
#  - seller name
#  - expiry date
#  - ref key(users)
#

class Item(ndb.Model):
    title = ndb.StringProperty(required=True)
    description = ndb.TextProperty(required=False)
    price = ndb.FloatProperty(required=True)
    expiry_date = ndb.DateTimeProperty(required=True)

    creation_time = ndb.DateTimeProperty(auto_now_add=True, required=True)
    seller = ndb.KeyProperty(required=True, kind=CustomUser)

    def edit(self, title, price, expiry_date, description):
        self.title = title
        self.price = float(price)
        self.expiry_time = expiry_date
        self.description = description
        logging.log(logging.INFO,"editing item")
        return self.put()

    def remove(self):
        self.key.delete()
        logging.log(logging.INFO,"deleted item")

    @classmethod
    def remove_item(cls, key):
        try:
            actual_key = ndb.Key(urlsafe=key)
            actual_key.delete()
            return True
        except:
            return False

    @classmethod
    def create_item(cls, title, price, seller, expiry_date, description=''):
        i = cls(title=title, price=float(price), expiry_date=expiry_date, description=description, seller=seller)
        return i.put()
        logging.log(logging.INFO,"creating item")
