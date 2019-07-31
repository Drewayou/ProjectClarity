import webapp2
import jinja2
import os
import json
import random
from google.appengine.api import users
from google.appengine.ext import ndb
import questions

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Aboutus(webapp2.RequestHandler):
    def get(self):
        Aboutus_html = the_jinja_env.get_template('Aboutus.html')
        self.response.write(Aboutus_html.render())

class Loginpg(webapp2.RequestHandler):
    def get(self):
        Loginpg_html = the_jinja_env.get_template('Loginpg.html')
        self.response.write(Loginpg_html.render())

class FirstPage(webapp2.RequestHandler):
    def get(self):
        First_html = the_jinja_env.get_template('first.html')
        self.response.write(First_html.render())

class ClarityUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    quiz_questions = ndb.JsonProperty()

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
            Login_html = the_jinja_env.get_template('Loginpg.html')
            login_url = users.create_login_url('/')
            login_dict={
            "login_url": login_url
            }
            self.response.write(Login_html.render(login_dict))
            self.response.write('Please log in.<br>' + login_html_element)


    def post(self):
        user = users.get_current_user()
        random.shuffle(questions.elements)
        clarity_user = ClarityUser(
            first_name = self.request.get('first name'),
            last_name = self.request.get('last name'),
            email = user.nickname(),
            quiz_questions = json.dumps(questions.elements, separators=(',', ':'))
            )

        clarity_user.put()
        self.response.write('Thanks for signing up, %s! <br><a href="/start">Next</a>' % clarity_user.first_name)

class QuizPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        quiz_taker = ClarityUser.query().filter(ClarityUser.email == user.nickname()).fetch()
        Quiz_html = the_jinja_env.get_template('quiz.html')
        problems = json.loads(quiz_taker[0].quiz_questions)
        variable_dict= {
        "question": problems.pop()
        }
        self.response.write(Quiz_html.render(variable_dict))

class ResultsCPage(webapp2.RequestHandler):
    def get(self):
        ResultsC_html = the_jinja_env.get_template('results_c.html')
        self.response.write(ResultsC_html.render())

class ResultsFPage(webapp2.RequestHandler):
    def get(self):
        ResultsF_html = the_jinja_env.get_template('results_f.html')
        self.response.write(ResultsF_html.render())

class ResultsBPage(webapp2.RequestHandler):
    def get(self):
        ResultsB_html = the_jinja_env.get_template('results_b.html')
        self.response.write(ResultsB_html.render())

class ResultsTPage(webapp2.RequestHandler):
    def get(self):
        ResultsT_html = the_jinja_env.get_template('results_t.html')
        self.response.write(ResultsT_html.render())

class ResultsDPage(webapp2.RequestHandler):
    def get(self):
        ResultsD_html = the_jinja_env.get_template('results_d.html')
        self.response.write(ResultsD_html.render())

class ResultsSPage(webapp2.RequestHandler):
    def get(self):
        ResultsS_html = the_jinja_env.get_template('results_s.html')
        self.response.write(ResultsS_html.render())



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/start', FirstPage),
    ('/quiz', QuizPage),
    ('/login', Loginpg),
    ('/results-c', ResultsCPage),
    ('/results-f', ResultsFPage),
    ('/results-b', ResultsBPage),
    ('/results-t', ResultsTPage),
    ('/results-d', ResultsDPage),
    ('/results-s', ResultsSPage),
    ('/about', Aboutus),
], debug=True)
