import webapp2
import jinja2
import os

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        First_html = the_jinja_env.get_template('first.html')
        self.response.write(First_html.render())

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
