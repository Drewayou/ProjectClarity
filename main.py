import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class FirstPage(webapp2.RequestHandler):
    def get(self):
        First_html = the_jinja_env.get_template('first.html')
        self.response.write(First_html.render())

class ClarityUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            signout_link_html = '<a href="%s">sign out</a>' % (
                    users.create_logout_url('/'))
            email_address = user.nickname()
            clarity_user = ClarityUser.query().filter(ClarityUser.email == email_address).get()
            if clarity_user:
                self.response.write(
                  'Looks like you\'re registered. Thanks for using our site!<br><a href="/start">Next</a><br>')
                self.response.write(signout_link_html)
            else:
                # Registration form for a first-time visitor:
                self.response.write('''
                    Welcome to our site, %s!  Please sign up! <br>
                    <form method="post" action="/">
                    <input type="text" name="first_name">
                    <input type="text" name="last_name">
                    <input type="submit">
                    </form><br> %s <br>
                    ''' % (email_address, signout_link_html))

        else:
          # If the user isn't logged in...
            login_url = users.create_login_url('/')
            login_html_element = '<a href="%s">Sign in</a>' % login_url
            self.response.write('Please log in.<br>' + login_html_element)


    def post(self):
        user = users.get_current_user()
        clarity_user = ClarityUser(
            first_name = self.request.get('first name'),
            last_name = self.request.get('last name'),
            email = user.nickname()
        )
        clarity_user.put()
        self.response.write('Thanks for signing up, %s! <br><a href="/start">Next</a>' % clarity_user.first_name)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/start', FirstPage)
], debug=True)
