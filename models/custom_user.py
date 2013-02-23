# custom_user.py - abstraction for user actions and data

import datetime
import time
import hashlib
import logging
import webapp2

from google.appengine.ext import ndb
from google.appengine.ext.ndb.model import KindError


class CustomUser(ndb.Model):
    email = ndb.StringProperty(required=True)
    password_hash = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    confirmed = ndb.BooleanProperty()
    date_created = ndb.DateTimeProperty()
    admin = ndb.BooleanProperty()
    active = ndb.BooleanProperty(required=True)

    # TODO enabled property
    # TODO user's items
    @webapp2.cached_property
    def items(self):
        """return all the items that belong to this user"""
        try:
            items = ndb.gql('SELECT * FROM Item WHERE seller = :1', self.key)
            logging.info('Getting items')
            return items
        except KindError:
            return None

    def confirm(self):
        self.confirmed=True
        self.active=True
        return self.put()

    def activate(self):
        self.active=True
        return self.put()

    def deactivate(self):
        self.active=False
        return self.put()

    def remove(self):
        # remove all objects associated with this user

        # remove items
        try:
            items = ndb.gql('SELECT * FROM Item WHERE seller = :1', self.key)
            def remove_item(item):
                item.remove()

            items.map(remove_item)
        except KindError:
            pass

        #TODO remove discussions, comments e.t.c


        # remove the account
        logging.info('removing account')
        self.key.delete()

    def make_admin(self):
        self.admin = True
        return self.put()

    def remove_admin(self):
        self.admin = False
        return self.put()

    @classmethod
    def enable_user(cls, key):
        try:
            user = ndb.Key(urlsafe=key).get()
            user.activate()
            return True
        except:
            return False

    @classmethod
    def disable_user(cls, key):
        try:
            user = ndb.Key(urlsafe=key).get()
            user.deactivate()
            return True
        except:
            return False

    @classmethod
    def make_user_admin(cls, key):
        try:
            user = ndb.Key(urlsafe=key).get()
            user.make_admin()
            return True
        except:
            return False

    @classmethod
    def remove_user_admin(cls, key):
        try:
            user = ndb.Key(urlsafe=key).get()
            user.remove_admin()
            return True
        except:
            return False

    @classmethod
    def get_by_key(cls, key):
        return ndb.Key(urlsafe=key).get()

    @classmethod
    def create_user(cls, email, password, name='', date_created=datetime.datetime.now()):
        new_user = cls(email=email, password_hash=password, name=name, confirmed=False, date_created=date_created, admin=False, active=False)
        return new_user.put()

    @classmethod
    def signup(cls, email, password, name=''):
        # get password hash
        password_hash = hashlib.sha1(password).hexdigest()

        # check if email exists in db
        users = cls.query(cls.email == email, cls.confirmed == True)
        if users.count() != 0:
            # there exists some users with that email
            return None

        # create user and save to db
        new_user = cls.create_user(email, password_hash, name)

        # craft token with current time and email
        token = hashlib.sha1(repr(time.time())+email).hexdigest()

        # save token
        CustomUserToken.create_token(new_user, token)

        # return token
        return token

    @classmethod
    def verify(cls, token):
        # get user id with matching token
        users = CustomUserToken.query(CustomUserToken.token == token)

        # if token exists
        if users.count() == 1:
            # set user confirmed
            user_token = users.get()

            user = user_token.user.get()
            confirmed_user_key = user.confirm()

            # remove token from db
            user_token.remove()

            # return confirmed user (for sessioning etc)
            return confirmed_user_key.get()

        # else return failure
        return None

    @classmethod
    def signin(cls, email, password):
        # get password hash
        password_hash = hashlib.sha1(password).hexdigest()
        users = CustomUser.query(CustomUser.email == email, CustomUser.password_hash == password_hash)

        # if user exists with matching email and password

        if users.count() != 1:
            return (None, 'not_found')

        u = users.get()

        if not u.active:
            return (None, 'active')

        return (u, 'ok')


class CustomUserToken(ndb.Model):
    user = ndb.KeyProperty(kind=CustomUser, required=True)
    token = ndb.StringProperty(required=True)

    def remove(self):
        self.key.delete()

    @classmethod
    def create_token(cls, user, token):
        t = cls(user=user, token=token)
        return t.put()
