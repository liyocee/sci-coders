# config.py - webapp2 configuration

import os

from models.custom_user import CustomUser

ROOT_PATH = os.path.join(os.path.dirname(__file__))

_config = {
    'production': True,
	'user_model' : CustomUser,
	'webapp2_extras.sessions': {
		'secret_key': '\xc1G\x9c\x0cM\xbe\xc8\xbf\x1d<l;.(\x880\xe54\xf3\n\xdd+k\x93'
	},
	'template_dir': os.path.join(ROOT_PATH,'templates'),
	'base_template': 'base/page.html', # Relative to the tempalates folder
}

def get_config():
	return _config
