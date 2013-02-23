__author__ = 'erico'
import logging

from google.appengine.ext import ndb

from views import BaseHandler, user_required, param_filter_and_escape
from models import discussion_models as dm
from models.custom_user import CustomUser
import datetime as dt

"""Contains all handlers involved in discussions"""


class DiscHome(BaseHandler):
    @user_required
    def get(self):
        k = self.user.key
        discs = dm.Discussion.query(ndb.OR(dm.Discussion.owner == k, dm.Discussion.participant == k))
        self.render_template('discussion_list.html', {'discussions': discs, 'user': k})


class DiscView(BaseHandler):
    @user_required
    def get(self, d_id):
        if d_id or d_id != '':
            d = None
            try:
                d = ndb.Key(urlsafe=d_id)
            except:
                self.abort(404, 'Discussion not found')
            disc = d.get()
            if disc is None:
                self.abort(404, 'Discussion not found.')
                #c = dm.Message.query(dm.Message.discussion == d)
            c = ndb.gql("select * from Message where discussion = :1", d)
            u = self.user
            self.render_template('discussion_comments.html', {'disc': disc, 'comms': c, 'user': u.key})


class DiscAdd(BaseHandler):
    @user_required
    def get(self):
        item_id = self.request.get('item')
        users = CustomUser.query()
        self.render_template('discussion_add.html', {'item': item_id, 'users': users, 'user': self.user.key})

    @user_required
    def post(self):
        topic = self.request.get('topic')
        to_id = self.request.get('to_id')
        participant = None
        topic = param_filter_and_escape(topic.strip())
        if len(topic) < 1:
            self.abort(400, 'Invalid topic name')
        try:
            participant = ndb.Key(urlsafe=to_id)
        except:
            self.abort(404, 'Participant not found')
        owner = self.user.key
        if owner == participant:
            self.abort(403, 'You cannot discuss with yourself')

        item_id = self.request.get('item')
        if item_id:
            item = None
            try:
                item = ndb.Key(urlsafe=item_id)
            except:
                self.abort(404, 'Item not found')
            item = item.get()
            if item.seller == self.user.key:
                self.abort(403, 'This is your item. You cannot discuss ')

        k = dm.Discussion.new(topic=topic, participant=participant, owner=owner, item=item_id)
        self.redirect(self.url_for('discussions view', d_id=k.urlsafe()))


class DiscDel(BaseHandler):
    @user_required
    def get(self, d_id):
        k = None
        try:
            k = ndb.Key(urlsafe=d_id)
        except:
            self.abort(404, 'Discussion not found')
        obj = k.get()
        if obj is None:
            self.redirect(self.url_for('discussions'))
            return
        if obj.owner != self.user.key:
            self.abort(403, 'You do not own the discussion thus you can\'t delete it')
        obj.remove()
        self.redirect(self.url_for('discussions'))


class DiscEdit(BaseHandler):
    @user_required
    def get(self, d_id):
        k = None
        try:
            k = ndb.Key(urlsafe=d_id)
        except:
            self.abort(404, 'Discussion not found')
        disc = k.get()
        if disc.owner != self.user.key:
            self.abort(403, 'You do not own the discussion thus you can\'t edit it')
        self.render_template('discussion_add.html', {'disc': disc, 'edit_mode': True})

    @user_required
    def post(self, d_id):
        topic = self.request.get('topic')
        k = None
        try:
            k = ndb.Key(urlsafe=d_id)
        except:
            self.abort(404, 'Discussion not found')
        disc = k.get()
        if disc.owner != self.user.key:
            self.abort(403, 'You do not own the discussion thus you can\'t edit it')
        topic = param_filter_and_escape(topic.strip())
        if len(topic) < 1:
            self.abort(400, 'Invalid topic name')
        if disc.topic != topic:
            disc.topic = topic
            disc.put()
        self.redirect(self.url_for('discussions view', d_id=k.urlsafe()))


#################### comment handlers ###################
class CommAdd(BaseHandler):
    @user_required
    def post(self, d_id):
        message = self.request.get("message")
        k = None
        try:
            k = ndb.Key(urlsafe=d_id)
        except:
            self.abort(404, 'Discussion not found')
        message = param_filter_and_escape(message.strip())
        if len(message) < 1:
            self.abort(400, 'Invalid topic name')

        disc = k.get()
        to = None
        if disc.owner == self.user.key:
            to = disc.owner
        else:
            to = disc.participant

        k = dm.Message.new(message=message, to=to, frm=self.user.key, discussion=k)
        self.redirect(self.uri_for('discussions view', d_id=d_id))
        msg = "from {0} , to {1} , datetime {2}".format(self.user.name, to.get().name, dt.datetime.now())
        if disc.item is not None:
            msg += " , item {0}".format(disc.item.get().title)
        logging.log(level=logging.INFO, msg=msg)



class CommEdit(BaseHandler):
    @user_required
    def get(self, c_id):
        pass

    @user_required
    def post(self, c_id):
        pass


class CommDel(BaseHandler):
    @user_required
    def get(self, c_id):
        k = None
        try:
            k = ndb.Key(urlsafe=c_id)
        except:
            self.abort(404, 'Message not found')

        mess = k.get()
        if mess is not None:
            d_id = mess.discussion
            if mess.frm != self.user.key:
                self.abort(404, "Message is not yours thus you can't delete it")
            mess.remove()
            self.redirect(self.uri_for('discussions view', d_id=d_id.urlsafe()))
        else:
            self.redirect(self.uri_for('discussions'))

