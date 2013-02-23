# usermodel.py - user account model

import time
import webapp2_extras.appengine.auth.models

from google.appengine.ext import ndb
from webapp2_extras import security

#User model
class User(ndb.Model):
    #user's name
    name = ndb.StringProperty(required=True)
    #user's username
    username = ndb.StringProperty(required=True)
    #user's **hashed** password. dibbs on sha1 :)
    password = ndb.StringProperty(required=True)
    #user's email address
    email = ndb.StringProperty(required=True)
    #user is activated
    active = ndb.BooleanProperty(default=False)
    #user is admin
    admin = ndb.BooleanProperty(default=False)
    #user's account is confirmed
    confirmed = ndb.BooleanProperty(default=False)

    @staticmethod
    def cur_user():
        a = User.query()
        if a.count() < 1:
            u = User(username='yusa', email='email@mail.com', name='name', password='pwd')
            u.put()
            return u
        return a.get()
