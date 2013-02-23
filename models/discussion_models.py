__author__ = 'erico'

from google.appengine.ext import ndb
from models.item_model import Item
from models.custom_user import CustomUser


class Discussion(ndb.Model):
    """A series of messages between a two parties"""
    topic = ndb.StringProperty()
    owner = ndb.KeyProperty(required=True, kind=CustomUser)
    participant = ndb.KeyProperty(required=True, kind=CustomUser)
    item = ndb.KeyProperty(required=False, kind=Item)
    time_created = ndb.DateTimeProperty(required=True, auto_now_add=True)

    def edit(self, topic):
        self.topic = topic
        self.put()

    def remove(self):
        #remove messages then remove discussion
        messages = ndb.gql("select * from Message where discussion = :1", self.key)
        for i in messages:
            i.remove()
        self.key.delete()

    @classmethod
    def new(cls, topic, owner, participant, item=''):
        d = cls(topic=topic, owner=owner, participant=participant)
        if item and item != '':
            i_key = ndb.Key(urlsafe=item)
            d.item = i_key
        return d.put()


class Message(ndb.Model):
    """A message in the discussion"""
    message = ndb.TextProperty(required=True)
    time_created = ndb.DateTimeProperty(required=True, auto_now_add=True)
    discussion = ndb.KeyProperty(required=True, kind=Discussion)
    to = ndb.KeyProperty(required=True, kind=CustomUser)
    frm = ndb.KeyProperty(required=True, kind=CustomUser)
    isread = ndb.BooleanProperty(default=False)

    def edit(self, message, to, frm):
        self.message = message
        self.to = to
        self.frm = frm
        self.put()

    def remove(self):
        self.key.delete()

    @classmethod
    def new(cls, message, to, frm, discussion, isread=True):
        obj = cls(message=message, to=to, frm=frm, discussion=discussion, isread=isread)
        return obj.put()
