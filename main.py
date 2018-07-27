import webapp2
import jinja2
import os

import datetime

import time
import logging
from time import sleep

jinja_current_dir = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)


EDUCATION_NAV = [
    # Button id      link path           display name
    ("Daycare",  "DaycareandPreschool", "Daycare and Preschool"),
    ("Secondary", "SecondarySchool ", "Secondary School"),
    ("Colleges", "CollegesandUniversities", "Colleges and Universities"),
    ("International", "InternationalandBoarding", "International and Boarding Schools"),
    ("Resources", "LearningResources", "Learning Resources")
]

IMMIGRATION_NAV = [

    ("Legal", "LegalResources", "Legal Resources"),
    ("Citizenship", "CitizenshipInfo", "Citizenship Information" ),
    ("Visa", "VisaInfo", "Visa Information"),
    ("StateInfo", "StateInfo", "State Specific Information"),

]

USLIFE_NAV = [
    ("InsuRance", "InsuranceP", "Insurance"),
    ("HouseInfo", "HousingP", "Housing"),
    ("HealthCare", "HealthC", "Healthcare Information"),
    ("BankFin", "BankFinan", "Bank and Financial Information"),
    ("Employmnt", "Employ", "Employment")
]

USCULTURE_NAV = [
    ("SlanG", "SlangP", "Slang"),
    ("PolChan", "PolCliP", "Political Climate"),
    ("SportS", "SportsP", "Sports"),
    ("HoliHist", "HolHisP", "Holidays and Historic Figures"),
    ("StateAt", "StateAttrP", "State Attractions"),
    ("GenTip", "GenTips", "General Tips")
]


from google.appengine.api import users
from google.appengine.ext import ndb

class CssiUser(ndb.Model):

  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  username = ndb.StringProperty()
  email = ndb.StringProperty()
  password = ndb.StringProperty()

  user_name = ndb.StringProperty()
  last_activity = ndb.DateTimeProperty()

class Question(ndb.Model):
    askerinfo = ndb.KeyProperty(CssiUser)
    timeasked = ndb.DateTimeProperty()
    # replies = ndb.KeyProperty(Reply, repeated=True)
    question = ndb.StringProperty()
    title = ndb.StringProperty()

class Reply(ndb.Model):
    timegiven = ndb.DateTimeProperty()
    giverinfo = ndb.KeyProperty(CssiUser)
    reply = ndb.StringProperty()
    question = ndb.KeyProperty(Question)

class ForumPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/forum.html")
        self.response.write(page_content.render())

class FormSubmit(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get("user_name")
        user = CssiUser.query(CssiUser.user_name == user_name)
        question = Question(askerinfo = user, timeasked = datetime.datetime.now(), question = self.request.get("question"), title = self.request.get("title"))


jinja_current_dir = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)

class MainHandler(webapp2.RequestHandler):
  def get(self):
    welcome_template = jinja_current_dir.get_template("Templates/signup_page.html")
    if self.request.cookies.get("loggen_in") == True:
        self.response.write(welcome_template.render(success =True, user = self.request.cookies.get("user")))

    else:
        self.response.write(welcome_template.render(failure = True))
    # If the user is logged in...
  def post(self):
    home_template = jinja_current_dir.get_template("Templates/signup_page.html")
    cssi_user = CssiUser(
    first_name = self.request.get('firstName'),
    last_name = self.request.get('lastName'),
    username = self.request.get('Username'),
    email = self.request.get('Email'),
    password = self.request.get('Password'))

    cssi_user.put()
    self.response.set_cookie("logged_in", "True")
    self.response.set_cookie("user", cssi_user.username)
    self.response.write(home_template.render(success = True, user = cssi_user.first_name))
    sleep(.5)
    self.redirect('/Login')



class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.response.delete_cookie("logged_in")
        self.response.delete_cookie("user")

        self.redirect('/')

class Dashboard(ndb.Model):
    button_save = ndb.StringProperty();
    actual_name = ndb.StringProperty();


# class HomeWithDashboardPage(webapp2.RequestHandler):
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        session = jinja_current_dir.get_template("Templates/signIn_page.html")
        self.response.write(session.render(start = True, error = False))

    def post(self):
        username = self.request.get("Username")
        password = self.request.get("Password")

        session_iniciada = False
        q = CssiUser.query().fetch()
        for user in q:
            if user.username == username and user.password == password:

                self.response.set_cookie("logged_in","True")
                self.response.set_cookie("user", user.username)
                self.response.clear()
                session_iniciada = True
                self.redirect('/Home')
                return

            else:
                session_iniciada = False
                self.response.delete_cookie("logged_in")
                self.response.delete_cookie("user")

        if not session_iniciada:
            not_session = jinja_current_dir.get_template("Templates/signIn_page.html")
            self.response.write(not_session.render(start = True, error = True, Username = username, Password = password))

        else:
            self.redirect("/Home")

class HomeWithDashboardPage(webapp2.RequestHandler):
    def post(self):
        home_template = jinja_current_dir.get_template("Templates/homePage.html")
        answer = self.request.get('answer')
        actual_name = self.request.get('submit')

        SaveData = Dashboard(button_save = answer, actual_name = actual_name)
        SaveData.put()
        # self.response.write(home_template.render(button_save = answer, actual_name = actual_name))
        self.redirect('/Home')
        # time.sleep(.15)
    def get(self):
        home_template = jinja_current_dir.get_template("Templates/homePage.html")

        if self.request.cookies.get("logged_in") == "True":
            dashboardData = CssiUser.query()
            self.response.write(home_template.render(active = True, dashboardData = dashboardData))
        # else:

        # self.response.write(home_template.render(dashboardData = dashboardData))
        #     self.response.write(home_template.render(login = True))
        # self.response.write()


class EducationPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/education.html")
        params = {
            'navbar_content': EDUCATION_NAV

        }
        self.response.write(page_content.render(params))

class DaycarePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/daycare.html")
        self.response.write(page_content.render(navbar_content=EDUCATION_NAV))

class SecondaryPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/secondary.html")
        self.response.write(page_content.render(navbar_content=EDUCATION_NAV))

class CollegePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/college.html")
        self.response.write(page_content.render(navbar_content = EDUCATION_NAV))

class InternationalPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/intl.html")
        self.response.write(page_content.render(navbar_content = EDUCATION_NAV))

class LearningPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/learning.html")
        self.response.write(page_content.render(navbar_content = EDUCATION_NAV))

class ImmigrationPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/immigration.html")
        params = {
            'navbar_content': IMMIGRATION_NAV
        }
        self.response.write(page_content.render(params))

class LegalPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/legal.html")
        self.response.write(page_content.render(navbar_content = IMMIGRATION_NAV))

class CitizenshipPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/citizenship.html")
        # navbar_content = jinja_current_dir.get_template("Templates/citizenship.html")
        self.response.write(page_content.render(navbar_content = IMMIGRATION_NAV))

class VisaPage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/visa.html")
        # navbar_content = jinja_current_dir.get_template("Templates/visa.html")
        self.response.write(page_content.render(navbar_content = IMMIGRATION_NAV))

class StatePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/state.html")
        # navbar_content = jinja_current_dir.get_template("Templates/state.html")
        self.response.write(page_content.render(navbar_content = IMMIGRATION_NAV))


class USLifePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/uslife.html")
        params = {
            'navbar_content':USLIFE_NAV
        }
        self.response.write(page_content.render(params))

class InsurancePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/insurance.html")
        self.response.write(page_content.render(navbar_content = USLIFE_NAV))

class HousingPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/housing.html")
        # navbar_content = jinja_current_dir.get_template("Templates/insurance.html")
        self.response.write(page_content.render(navbar_content = USLIFE_NAV))

class HealthCare(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/healthCare.html")
        # navbar_content = jinja_current_dir.get_template("Templates/healthCare.html")
        self.response.write(page_content.render(navbar_content = USLIFE_NAV))

class BankAndFinancial(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/financial.html")
        self.response.write(page_content.render(navbar_content = USLIFE_NAV))

class Employment(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/employment.html")
        self.response.write(page_content.render(navbar_content = USLIFE_NAV))

class CulturePage (webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/culture.html")
        params = {
            'navbar_content': USCULTURE_NAV
        }
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class SlangPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/slang_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class EtiquettePage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/etiquette_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class PoliticalClimatePage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/politicalClimate_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class SportsPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/sports_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class HolidaysAndHistoryPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/holidaAndHistory.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class StateAttraction(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/stateAtractions_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class GeneralTipsPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/genTips_page.html")
        self.response.write(page_content.render(navbar_content = USCULTURE_NAV))

class ForumPage(webapp2.RequestHandler):
    def get(self):
        page_content = jinja_current_dir.get_template("Templates/forum.html")
        self.response.write(page_content.render())

class FormSubmit(webapp2.RequestHandler):
    def get(self):
        print self.request.get("firstname")

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        welcomePage_content = jinja_current_dir.get_template("Templates/welcome1.html")
        self.response.write(welcomePage_content.render())


app = webapp2.WSGIApplication([
  ('/Login', LoginHandler),
  ('/', MainHandler),
  ('/welcome', WelcomePage),
  ('/Home', HomeWithDashboardPage),
  ('/Education', EducationPage),
  ('/Immigration', ImmigrationPage),
  ('/USLife', USLifePage),
  ('/USCulture', CulturePage),
  ('/DaycareandPreschool', DaycarePage),
  ('/SecondarySchool', SecondaryPage),
  ('/CollegesandUniversities', CollegePage),
  ('/InternationalandBoarding', InternationalPage),
  ('/LearningResources', LearningPage),
  ('/InsuranceP', InsurancePage),
  ('/HousingP', HousingPage),
  ('/HealthC', HealthCare),
  ('/BankFinan', BankAndFinancial),
  ('/Employ', Employment),
  ('/LegalResources', LegalPage),
  ('/CitizenshipInfo', CitizenshipPage),
  ('/VisaInfo', VisaPage),
  ('/StateInfo', StatePage),
  ('/SlangP', SlangPage),
  ('/EtiqP', EtiquettePage),
  ('/PolCliP', PoliticalClimatePage),
  ('/SportsP', SportsPage),
  ('/HolHisP', HolidaysAndHistoryPage),
  ('/StateAttrP', StateAttraction),
  ('/GenTips', GeneralTipsPage),
  ('/Forum', ForumPage),
  ('/formsubmit', FormSubmit)
], debug=True)
