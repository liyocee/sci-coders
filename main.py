# main.py - main starting point of app
import webapp2

import routes # app url routes
import config # webapp2 configuration

app = webapp2.WSGIApplication(routes.get_routes(), config=config.get_config(),debug=True)
