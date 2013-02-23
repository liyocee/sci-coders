"""Contains all handlers fo items and item management"""

import logging

from datetime import datetime as dt

from google.appengine.ext import ndb

from views import BaseHandler, user_required, param_filter_and_escape
from models.item_model import Item


class Items(BaseHandler):
    """List all items in datastore"""

    def get(self):
        i = Item.query()
        u = self.user
        if u is not None:
            self.render_template('items.html', {'items': i, 'user': self.user.key})
        else:
            self.render_template('items.html', {'items': i})


class ItemAdd(BaseHandler):
    """Add a new item"""

    @user_required
    def get(self):
        self.render_template('item_add.html')

    @user_required
    def post(self):
        title = param_filter_and_escape(self.request.POST['txtTitle'])
        price = param_filter_and_escape(self.request.POST['txtPrice'])
        exp_d = param_filter_and_escape(self.request.POST['txtExpiryD'])
        exp_t = param_filter_and_escape(self.request.POST['txtExpiryT'])
        desc = param_filter_and_escape(self.request.POST['txtDesc'])

        time = "{0} {1}".format(exp_d, exp_t)
        time = dt.strptime(time, '%Y-%m-%d %H:%M')
        if time < dt.now():
            self.abort(400, 'Sorry the expiry time set is in the past')

        u = self.user
        Item.create_item(title, price, u.key, time, desc)

        self.redirect(self.uri_for('items'))


class ItemEdit(BaseHandler):
    """
    edit items given their urlsafe_id
    get method shows the edit form and the data for that
    post method saves the info
    """

    @user_required
    def get(self, *args, **kwds):
        i_id = kwds['id']
        try:
            key = ndb.Key(urlsafe=i_id)
            it = key.get()
            user = self.user

            # check if the item being edited belongs to the user
            if it.seller != user.key:
                self.abort(403, 'Sorry, you cannot edit items that do not belong to you')
                return

            # TODO pass item object
            data = {
                'item': it,
                'edit_mode': True,
                'item_id': i_id,
            }

            self.render_template('item_add.html', data)
        except BaseException, e:
            logging.info("ERROR: " + repr(e))
            self.redirect(self.uri_for('items'))

    @user_required
    def post(self, *args, **kwds):
        id = kwds['id']
        key = None
        try:
            key = ndb.Key(urlsafe=id)
        except:
            self.abort(404, 'Item not found')
        obj = key.get()

        user = self.user

        if obj.seller != user.key:
            self.abort(400, 'Sorry, you cannot edit items that do not belong to you')
            return

        changed = param_filter_and_escape(self.request.POST['changed'])
        title = param_filter_and_escape(self.request.POST['txtTitle'])
        price = param_filter_and_escape(self.request.POST['txtPrice'])
        exp_d = param_filter_and_escape(self.request.POST['txtExpiryD'])
        exp_t = param_filter_and_escape(self.request.POST['txtExpiryT'])
        desc = param_filter_and_escape(self.request.POST['txtDesc'])

        time = "{0} {1}".format(exp_d, exp_t)
        time = dt.strptime(time, '%Y-%m-%d %H:%M:%S')
        if time < dt.now():
            self.abort(403, 'Sorry the expiry time set is in the past')

        obj.edit(title, price, time, desc)

        self.redirect(self.uri_for('items'))


class ItemDel(BaseHandler):
    """delete items given their urlsafe_id"""

    def get(self, *args, **kwargs):
        id = kwargs['id']
        key = None
        try:
            key = ndb.Key(urlsafe=id)
        except:
            self.abort(404, 'Item not found')
        key.delete()

        self.redirect(self.uri_for('items'))
