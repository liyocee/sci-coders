from views import BaseHandler

class HelloWorld(BaseHandler):
	''' simple example handler '''
	
	def get(self):
		user = self.auth.get_user_by_session()
		params = {
			'user': user
		}
		self.render_template("hello.html", params)
