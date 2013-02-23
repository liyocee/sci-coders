# home.py - Home Page

from views import BaseHandler

class HomeHandler(BaseHandler):
	def get(self):
		params = {
			#'user_info': self.user_info,
			'user': self.user
		}
		self.render_template('home.html', params)
