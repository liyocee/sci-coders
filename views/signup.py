# signup.py - handle signup requests

from views import BaseHandler

class SignUp(BaseHandler):
	
	def get(self):
		user = self.get_current_user()
		if user:
			self.redirect(self.uri_for('home'))
			return
		self.render_template('signup.html')
	
	def post(self):
		user = self.get_current_user()
		if user:
			self.redirect(self.uri_for('home'))
			return
		name = self.request.get('name')
		email = self.request.get('email')
		username = self.request.get('username')
		password = self.request.get('password')
		
		unique_properties = ['email_address']
		user_data = self.user_model.create_user(name,
			unique_properties,
			email_address=email, name=name, password_raw=password,
			admin=False, active=False, confirmed=False)
		
		if not user_data[0]:
			self.display_message('Unable to create user for email %s because of \
				duplicate keys %s' % (user_name, user_data[1]))
			return
		
		user = user_data[1]
		user_id = user.get_id()
		
		token = self.user_model.create_signup_token(user_id)
		
		verification_url = self.uri_for('verification', type='v', user_id=user_id,
			signup_token=token, _full=True)		
		
		msg = 'Verify with <a href="%s">%s</a>'
		
		self.display_message(msg % (verification_url,verification_url))
