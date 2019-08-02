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

class Relationships(ndb.Model):
    name = ndb.StringProperty()
    status = ndb.StringProperty()

class ClarityUser(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    quiz_questions = ndb.JsonProperty()
    ccount = ndb.IntegerProperty()
    fcount = ndb.IntegerProperty()
    bcount = ndb.IntegerProperty()
    tcount = ndb.IntegerProperty()
    dcount = ndb.IntegerProperty()
    scount = ndb.IntegerProperty()
    results = ndb.KeyProperty(Relationships,repeated=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            #signout_link_html = '<a href="%s">sign out</a>' % (
            #        users.create_logout_url('/')
            signout_link_html = users.create_logout_url('/')
            email_address = user.nickname()
            clarity_user = ClarityUser.query().filter(ClarityUser.email == email_address).get()
            if clarity_user:
                Registree_html = the_jinja_env.get_template('register2.html')
                variable_dict= {
                "signout": signout_link_html,
                "username": clarity_user.first_name
                }
                self.response.write(Registree_html.render(variable_dict))
                #self.response.write(
                #  'Looks like you\'re registered. Thanks for using our site!<br><a href="/start">Next</a><br>')
                #self.response.write(signout_link_html)
            else:
                # Registration form for a first-time visitor:
                Register_html = the_jinja_env.get_template('register1.html')
                variable_dict= {
                "email": email_address,
                "signout": signout_link_html
                }
                self.response.write(Register_html.render(variable_dict))
                #self.response.write('''
                #    Welcome to our site, %s!  Please sign up! <br>
                #    <form method="post" action="/">
                #    <input type="text" name="first_name">
                #    <input type="text" name="last_name">
                #    <input type="submit">
                #    </form><br> %s <br>
                #    ''' % (email_address, signout_link_html))

        else:
          # If the user isn't logged in...
            login_url = users.create_login_url('/')
            #login_html_element = '<a href="%s">Sign in</a>' % login_url
            Login_html = the_jinja_env.get_template('signin.html')
            #login_url = users.create_login_url('/')
            login_dict={
            "login_site": login_url
            }
            self.response.write(Login_html.render(login_dict))
            #self.response.write('Please log in.<br>' + login_html_element)


    def post(self):
        user = users.get_current_user()
        random.shuffle(questions.elements)
        clarity_user = ClarityUser(
            first_name = self.request.get('first_name'),
            last_name = self.request.get('last_name'),
            email = user.nickname(),
            quiz_questions = json.dumps(questions.elements, separators=(',', ':')),
            ccount = 0,
            fcount = 0,
            bcount = 0,
            tcount = 0,
            dcount = 0,
            scount = 0,
            )

        clarity_user.put()

        signout_link_html = users.create_logout_url('/')
        Thankyou_html = the_jinja_env.get_template('signup.html')
        variable_dict= {
        "signout": signout_link_html,
        "username": clarity_user.first_name
        }
        self.response.write(Thankyou_html.render(variable_dict))
        #self.response.write('Thanks for signing up, %s! <br><a href="/start">Next</a>' %clarity_user.first_name)

class QuizPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        quiz_taker = ClarityUser.query().filter(ClarityUser.email == user.nickname()).fetch()
        Quiz_html = the_jinja_env.get_template('quiz.html')
        problems = json.loads(quiz_taker[0].quiz_questions)
        variable_dict= {
        "question": problems[0],
        "index": 0
        }
        self.response.write(Quiz_html.render(variable_dict))
    def post(self):
        user = users.get_current_user()
        quiz_taker = ClarityUser.query().filter(ClarityUser.email == user.nickname()).fetch()
        Quiz_html = the_jinja_env.get_template('quiz.html')
        problems = json.loads(quiz_taker[0].quiz_questions)
        crush = quiz_taker[0].ccount
        friend = quiz_taker[0].fcount
        bestie = quiz_taker[0].bcount
        talking = quiz_taker[0].tcount
        dating = quiz_taker[0].dcount
        serious = quiz_taker[0].scount
        selection1 = self.request.get('answer-choice')

        if selection1 == "s":
            serious += 1
        elif selection1 == "d":
            dating += 1
        elif selection1 == "t":
            talking += 1
        elif selection1 == "b":
            bestie += 1
        elif selection1 == "f":
            friend += 1
        elif selection1 == "c":
            crush += 1

        problem_index = self.request.get('problem-index')
        new_index = int(problem_index) + 1

        if new_index < 10:
            variable_dict= {
            "question": problems[new_index],
            "index": new_index
            }
            self.response.write(Quiz_html.render(variable_dict))
        else:
            category_counts = [crush, friend, bestie, talking, dating, serious]
            max_count = max(category_counts)
            result_page = ''
            if max_count == crush:
                result_page = 'results_c.html'
            elif max_count == friend:
                result_page = 'results_f.html'
            elif max_count == bestie:
                result_page = 'results_b.html'
            elif max_count == talking:
                result_page = 'results_t.html'
            elif max_count == dating:
                result_page = 'results_d.html'
            else:
                result_page = 'results_s.html'
            Results_html = the_jinja_env.get_template(result_page)
            self.response.write(Results_html.render())

class ResultsCPage(webapp2.RequestHandler):
    def get(self):
        ResultsC_html = the_jinja_env.get_template('results_c.html')
        self.response.write(ResultsC_html.render())
    def post(self):
        print("Hello")

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

class Logoutpg(webapp2.RequestHandler):
    def get(self):
        Logoutpg_html = the_jinja_env.get_template('Logoutpg.html')
        self.response.write(Logoutpg_html.render())

class Gallerypg(webapp2.RequestHandler):
    def get(self):
        Gallery_html= the_jinja_env.get_template('gallery.html')
        user = users.get_current_user()
        quiz_taker = ClarityUser.query().filter(ClarityUser.email == user.nickname()).fetch()
        variable_dict = {
            'quizresults': quiz_taker[0].results
        }
        self.response.write(Gallery_html.render(variable_dict))
    def post(self):
        Gallery_html= the_jinja_env.get_template('gallery.html')
        user = users.get_current_user()
        quiz_taker = ClarityUser.query().filter(ClarityUser.email == user.nickname()).fetch()
        each_result = Relationships(
        name = self.request.get('their_name'),
        status = self.request.get('realstatus')
        )
        each_result_key = each_result.put()
        quiz_taker[0].results.append(each_result_key)
        quiz_taker[0].put()
        variable_dict = {
            'quizresults': quiz_taker[0].results
        }
        self.response.write(Gallery_html.render(variable_dict))

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
    ('/logout', Logoutpg),
    ('/gallery', Gallerypg),
], debug=True)
