#show all items for user

import logging

from datetime import datetime as dt

from google.appengine.ext import ndb


from views import BaseHandler, user_required, param_filter_and_escape

from models.item_model import Item
import keyword

class Browse(BaseHandler):
    def get(self):
        i = Item.query()
        data = {
            'items': i,
            'user_info': self.user_info
        }
        self.render_template('search.html', data)

# Search for items

class Search(BaseHandler):
    @user_required
    def get(self):
        criteria = param_filter_and_escape(self.request.get('criteria'))
        keyword = param_filter_and_escape(self.request.get('keyword'))
        SearchItems = []        
        
        if criteria and keyword:

            if(criteria=='Title'):
                SearchItems = Item.query(Item.title == keyword)
            elif (criteria=='Description'):
                SearchItems = Item.query(Item.description == keyword)
            elif (criteria=='Price'):
                try:
                    SearchItems = Item.query(Item.price == float(keyword))
                except:
                    pass
            else:
                pass
                
        data = {
            'user_info': self.user_info,
            'SearchItems':SearchItems
        }
                
        self.render_template('search.html', data)
        
