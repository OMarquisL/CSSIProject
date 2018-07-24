import webapp2
import jinja2
import os


from google.appengine.api import users
from google.appengine.ext import ndb

class CssiUser(ndb.Model):
  """CssiUser stores information about a logged-in user.

  The AppEngine users api stores just a couple of pieces of
  info about logged-in users: a unique id and their email address.

  If you want to store more info (e.g. their real name, high score,
  preferences, etc, you need to create a Datastore model like this
  example).
  """
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()

jinja_current_dir = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)

class MainHandler(webapp2.RequestHandler):

  def get(self):
    welcome_template = jinja_current_dir.get_template("Templates/index.html")
    self.response.write(welcome_template.render())
    user = users.get_current_user()

    # If the user is logged in...
    if user:
      email_address = user.nickname()
      cssi_user = CssiUser.get_by_id(user.user_id())
      signout_link_html = '<a href="%s">sign out</a>' % (
          users.create_logout_url('/'))
      # If the user has previously been to our site, we greet them!
      if cssi_user:
        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              cssi_user.first_name,
              cssi_user.last_name,
              email_address,
              signout_link_html))
      # If the user hasn't been to our site, we ask them to sign up
      else:
        self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/">
            <input type="text" name="first_name">
            <input type="text" name="last_name">
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, signout_link_html))
    # Otherwise, the user isn't logged in!
    else:
      self.response.write('''
        Please log in to use our site! <br>
        <a href="%s">Sign in</a>''' % (
          users.create_login_url('/')))

  def post(self):
    bye_template = jinja_current_dir.get_template("Templates/bye.html")
    self.response.write(bye_template.render())
    user = users.get_current_user()
    if not user:
      # You shouldn't be able to get here without being logged in
      self.error(500)
      return
    cssi_user = CssiUser(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        id=user.user_id())
    cssi_user.put()
    self.response.write('Thanks for signing up, %s!' %
        cssi_user.first_name)


class HomePage(webapp2.RequestHandler):
    def get(self):
        home_template = jinja_current_dir.get_template("Templates/homePage.html")
        self.response.write(home_template.render())
    #def post(self):


class Education(webapp2.RequestHandler):
    def get(self):
        education_template = jinja_current_dir.get_template("Templates/education.html")
        self.response.write(education_template.render())

class Immigration(webapp2.RequestHandler):
    def get(self):
        immigration_template = jinja_current_dir.get_template("Templates/immigration.html")
        self.response.write(immigration_template.render())

class LivingInUS(webapp2.RequestHandler):
    def get(self):
        usaLifestyle_template = jinja_current_dir.get_template("Templates/usLifestyle.html")
        self.response.out.write(usaLifestyle_template.render())


app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/Home', HomePage),
  ('/Educ', Education),
  ('/Immi', Immigration),
  ('/USLS', LivingInUS),

], debug=True)
