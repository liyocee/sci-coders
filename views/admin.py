# admin handlers

from views import BaseHandler, admin_required
from models.item_model import Item

class SuperAdminHandler(BaseHandler):
    """ show super admin interface """
    
    def get(self):
        self.redirect(self.uri_for('admin'))

class AdminHandler(BaseHandler):
    """ show unified admin interface """
    
    @admin_required
    def get(self):
        # show admin interface
        
        params ={
            'users': self.user_model.query(),
            'items': Item.query(),
            'uri_for': self.uri_for,
            'is_superadmin': self.is_superadmin,
            'current_user': self.user,
        }
        
        self.render_template('admin.html', params)


class AdminRemoveItemHandler(BaseHandler):
    """ remove items with prejudice """
    
    @admin_required
    def get(self, *args, **kwds):
        # get item key
        id = kwds['id']
        if not Item.remove_item(id):
            # show error message
            self.display_message('Sorry that item could not be deleted. <a href="%s">Back to admin</a>' % self.uri_for('admin'))
            return
        
        self.redirect(self.uri_for('admin'))
        
class AdminAdd(BaseHandler):
    """ make another user admin """
    
    @admin_required
    def get(self, *args, **kwds):
        # get user
        id = kwds['id']
        if not self.user_model.make_user_admin(id):
            # show error message
            self.display_message('Sorry, could not make that user an admin. <a href="%s">Back to admin</a>' % self.uri_for('admin'))
            return
        
        self.redirect(self.uri_for('admin'))

class AdminRemove(BaseHandler):
    """ remove a user's admin status """
    
    @admin_required
    def get(self, *args, **kwds):
        # get user
        id = kwds['id']
        if not self.user_model.remove_user_admin(id):
            # show error message
            self.display_message('Sorry, could not remove that user\'s admin capabilities. <a href="%s">Back to admin</a>' % self.uri_for('admin'))
            return
        
        self.redirect(self.uri_for('admin'))

class AdminDisable(BaseHandler):
    """ disable a user account """
    
    @admin_required
    def get(self, *args, **kwds):
        id = kwds['id']
        if not self.user_model.disable_user(id):
            # show error message
            self.display_message('Sorry, could not deactivate that user. <a href="%s">Back to admin</a>' % self.uri_for('admin'))
            return
        
        self.redirect(self.uri_for('admin'))

class AdminEnable(BaseHandler):
    """ enable a user account """
    
    @admin_required
    def get(self, *args, **kwds):
        id = kwds['id']
        if not self.user_model.enable_user(id):
            # show error message
            self.display_message('Sorry, could not activate that user. <a href="%s">Back to admin</a>' % self.uri_for('admin'))
            return
        
        self.redirect(self.uri_for('admin'))


class SuperAdminSignOut(BaseHandler):
    """ sign out superuser """
    
    def get(self):
        self.signout_superadmin()
