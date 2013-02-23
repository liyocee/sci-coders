# __init__.py - common classes, functions and data across view handlers

import cgi

import webapp2
import jinja2
from webapp2_extras import sessions
from google.appengine.api import users as api_users

from bs4 import BeautifulSoup


acceptable_elements = ['a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
                       'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
                       'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
                       'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                       'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol',
                       'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
                       'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                       'thead', 'tr', 'tt', 'u', 'ul', 'var']

acceptable_attributes = ['abbr', 'accept', 'accept-charset', 'accesskey',
                         'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
                         'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
                         'colspan', 'color', 'compact', 'coords', 'datetime', 'dir',
                         'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
                         'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
                         'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt',
                         'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
                         'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
                         'usemap', 'valign', 'value', 'vspace', 'width']


def param_escape(to_be_san):
    return cgi.escape(to_be_san)


def param_filter(fragment):
    while True:
        soup = BeautifulSoup(fragment)
        removed = False
        for tag in soup.findAll(True): # find all tags
            if tag.name not in acceptable_elements:
                tag.extract() # remove the bad ones
                removed = True
            else: # it might have bad attributes
                # a better way to get all attributes?
                for attr in tag._getAttrMap().keys():
                    if attr not in acceptable_attributes:
                        del tag[attr]

        # turn it back to html
        fragment = unicode(soup)

        if removed:
            # we removed tags and tricky can could exploit that!
            # we need to reparse the html until it stops changing
            continue # next round

        return fragment


def param_filter_and_escape(fragment):
    return param_escape(param_filter(fragment))

# basehandlers
class TemplateHandler(webapp2.RequestHandler):
    def render_template(self, filename,
                        template_values={}, **template_args):
        """outputs a rendered jinja template"""
        jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.app.config.get('template_dir')))
        template = jinja_environment.get_template(filename)

        # add base template variable
        template_values['__base_template'] = self.app.config.get('base_template')

        self.response.out.write(template.render(template_values))


class SessionHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session(backend='datastore')

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)


class CustomHandler(TemplateHandler):
    def display_message(self, content):
        params = {
            'message': content,
        }
        self.render_template('message.html', params)


class AuthenticatedHandler(SessionHandler):
    @webapp2.cached_property
    def user_info(self):
        if 'user_info' in self.session:
            return self.session['user_info']

        return None

    @webapp2.cached_property
    def user(self):
        if self.user_info and 'id' in self.user_info:
            return self.user_model.get_by_id(self.user_info['id'])

        return None

    @webapp2.cached_property
    def user_model(self):
        return self.app.config.get('user_model')

    @webapp2.cached_property
    def is_admin(self):
        return self.is_superadmin or self.user.admin

    @webapp2.cached_property
    def is_superadmin(self):
        return api_users.is_current_user_admin()

    def add_to_session(self, user):
        # TODO add session tokens
        user_info = {
            'name': user.name,
            'id': user.key.id(),
        }

        self.session['user_info'] = user_info

    def remove_from_session(self):
        if 'user_info' in self.session:
            del self.session['user_info']

    def signout_superadmin(self):
        # BUG if non admin logins thru google they'll still remain logged in after being rejected
        if self.is_superadmin or api_users.get_current_user:
            self.redirect(api_users.create_logout_url(self.uri_for('signout')))
        else:
            self.abort(404)


def user_required(handler):
    def check_login(self, *args, **kwargs):
        if not self.user_info and not self.is_superadmin:
            self.redirect(self.uri_for('signin'), abort=True)
        else:
            return handler(self, *args, **kwargs)

    return check_login


def admin_required(handler):
    def check_admin_login(self, *args, **kwargs):
        # check if user is logged in and is an admin

        # if user is not logged in or is not superuser (who has no login support..ouch)
        if not self.user_info and not self.is_superadmin:
            self.redirect(self.uri_for('signin'), abort=True)
        # if user is logged in but not admin
        elif not self.is_admin:
            self.redirect(self.uri_for('home'), abort=True)
        # user must be admin by now
        else:
            return handler(self, *args, **kwargs)

    return check_admin_login


# collective base handler
class BaseHandler(CustomHandler, AuthenticatedHandler):
    # TODO add new render template here to cater for user details in templates, 
    # u can just add user_info (instead of user) which will confirm if someone's 
    # logged in or not
    def render_template(self, filename, template_values={}, **template_args):
        """add user_info to template arguments"""
        template_values['user_info'] = self.user_info
        super(BaseHandler, self).render_template(filename=filename, template_values=template_values, template_args=template_args)
