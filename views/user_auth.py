# user_authentication.py - all user authentication here

import webapp2
import logging

from google.appengine.api import mail, app_identity
from views import BaseHandler, user_required

def already_signed_in(handler):
    """ if signed in redirect to home """
    def check_signed_in(self, *args, **kwds):
        if self.user_info:
            self.redirect(self.uri_for('home'), abort=True)
        else:
            handler(self, *args, **kwds)
    
    return check_signed_in

class SignUpHandler(BaseHandler):
    """ handle signups """
    
    @already_signed_in
    def get(self):
        self.show_signup_form()

    @already_signed_in    
    def post(self):
        # get fields
        email = self.request.get('email')
        password = self.request.get('password')    
        confirm_password = self.request.get('confirm_password')
        name = self.request.get('name')
        
        # validate
        if not email or not password or password != confirm_password:
            # show signup form again
            params = {
                'email': email,
                'mismatch': password != confirm_password,
                'password': password,
                'name': name,
            }
            
            self.show_signup_form(True, params)
            return
        
        # if everything's fine, signup
        verification_token = self.user_model.signup(email, password, name)
        
        if not verification_token:
            # show signup form again
            params = {
                'email': email,
                'password': password,
                'name': name,
                'exists': True,
            }
            
            self.show_signup_form(True, params)
            return
        
        verification_url = self.uri_for('verify', token=verification_token, _full=True)
        
        if self.app.config.get('production'):
            # send verification url thru email
            app_id = app_identity.get_application_id()
            sender = "Hardcode SCI <noreply@%s.appspotmail.com" % app_id
            subject = "Verify your account"
            
            message = mail.EmailMessage(sender=sender, subject=subject)        
            message.to = "%s <%s>" % (name, email)
            message.body = """
            Hey %s,
            
            Your account was successfully created. All we need is for you to verify it here:
            
            %s
            
            If you have any questions, please get in touch with us through the site (dont reply to this message),
            
            Hardcode SCI team.
            """ % (name, verification_url)
            
            logging.info("Sending email: Sender: %s, Subject: %s, To: %s, Body: %s" % (message.sender, message.subject, message.to, message.body))
            
            message.send()
            
            self.display_message('Your account was successfully created. Please check your email to confirm your registration.')
        else:    
            # send verification token (test - just display)
            self.display_message('Verify using this link <a href="%s">Verify</a>' % verification_url)
        
    def show_signup_form(self, failed=False, params={}):
        """ shows empty or error state sign up form """
        params['failed'] = failed
        self.render_template('signup.html', params)

class VerificationHandler(BaseHandler):
    """ handler signup verifications """
    
    @already_signed_in
    def get(self, *args, **kwds):
        token = kwds['token']
        
        user = self.user_model.verify(token)
        
        # if token is invalid
        if not user:
            # show failure
            params = {
                'success': False,
            }
            
            self.render_template('verified.html', params)
            return
        
        # if token is valid
        
        # add user to session (sign in)
        self.add_to_session(user)
        
        # show success
        params = {
            'success': True,
        }
        
        self.render_template('verified.html', params)

class SignInHandler(BaseHandler):
    """ handles signin """
    
    @already_signed_in
    def get(self):
        # show sign in form
        self.show_sign_in_form()
    
    @already_signed_in
    def post(self):
        # get email and password fields
        email = self.request.get('email')
        password = self.request.get('password')
        
        # validate fields
        if not email or not password:
            params = {
                'email': email,
                'password': password,
            }
            
            self.show_sign_in_form(True, params)
            return
        
        # find user
        user = self.user_model.signin(email, password)
        
        # if no user
        if not user[0]:
            params = {
                'email': email,
                'password': password,
            }
            
            if user[1] == 'active':
                params['not_active'] = True
            
            if user[1] == 'not_found':
                params['not_found'] = True
            
            self.show_sign_in_form(True, params)
            return
        
        # if user
        self.add_to_session(user[0])
        
        # redirect to home
        self.redirect(self.uri_for('home'))
    
    def show_sign_in_form(self, failed=False, params={}):
        params['failed'] = failed
        self.render_template('signin.html', params)

class SignOutHandler(BaseHandler):
    """ handles signing out """
    
    def get(self):
        self.remove_from_session()
        self.redirect(self.uri_for('home'))

class ProfileHandler(BaseHandler):
    """ shows the user his profile page """
    
    @user_required
    def get(self, *args, **kwds):
        user_id = kwds['id'] if 'id' in kwds else None
        
        if user_id:
            # show that user's profile
            
            user = self.user_model.get_by_key(user_id)
            
            # check if user exists
            if not user:
                self.abort(404, "Sorry, that user does not exist.")
                return
            
            # show profile page with other user's details
            
            params = {
                'user': user,
                'current_user': False,
                'is_admin': self.is_admin,
            }
            
            self.render_template('profile.html', params)
            return
            
        # show current user's profile
        
        user = self.user
        
        params = {
            'user': user,
            'current_user': True,
        }
        
        self.render_template('profile.html', params)

class RemoveAccountHandler(BaseHandler):
    """ handles users removing their accounts, permanently """
    
    @user_required
    def get(self):
        # delete the account
        self.user.remove()
        
        # signout
        self.redirect(self.uri_for('signout'))
