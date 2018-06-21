# Global Modules
import web
import templates
import json


# Custom Modules
import users

# Direct function import
from users import *
from auth import handler
from sessionOps import SessionMgr
from webObjs import Objs
from bson import ObjectId
from templates import render

# Globals
urls = (
	"/", "Index",
	"/landing", "Landing",
	"/locked", "Locked",
	"/login", "LoginPage",
	"/register", "Register",
	"/logout", "Logout",
	"/auth/google", "AuthPage",
	"/auth/google/callback", "AuthCallbackPage",
	"/player", "Player",
	"/getObj", "GetObj",
	)
	
	
app = web.application( urls, globals())

class JSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, ObjectId):
			return str(o)
		return json.JSONEncoder.default(self, o)
		
class Landing:
 	def GET(self):
		return render("landing.html")
		
class Index:
	@users.login_required
	def GET(self):
		return render("index.html")
		
class Player:
	@users.login_required
	def GET(self):
		return JSONEncoder().encode(users.getUser())
		
class GetObj(Objs):
	@users.login_required
	def GET(self):
		print web.input()
		return JSONEncoder().encode(self._getObj(web.input('col')))

class AuthPage(handler):
	def GET(self):
		self._oauth2_init()

class AuthCallbackPage(handler):
	def GET(self):
		self._oauth2_callback()

class LoginPage:
	def GET(self):
		raise web.seeother('/auth/google')
			
class Register:
	def GET(self):
		return render("register.html")
	
	def POST(self):
		print "Register called"
		newUser(web.input(_method='POST'))
		print "Done with new User"
		
class Logout(SessionMgr):
	def GET(self):
		self.killSession()
		raise web.seeother('/')
		

class Locked:
	def GET(self):
		print web.input()
		return render("locked.html")

		
if __name__=="__main__":
    # web.internalerror = web.debugerror
    app.run()

