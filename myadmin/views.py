from myadmin.forms import *
from myadmin.auth import *
from myadmin.documents import *
from flask.ext.admin import BaseView, expose, AdminIndexView, base
from flask import render_template, redirect, url_for, flash, request
from flask.ext.admin.contrib import sqlamodel

class MyView(BaseView):
	@expose('/')
	def index(self):
		return self.render('index.html')

class LoggedUserIndexView(BaseView):
	def is_accessible(self):
		return login.current_user.is_authenticated()

	@expose('/')
	def index(self):
		return self.render('welcome.html')

class LogoutView(BaseView):
	def is_accessible(self):
		return login.current_user.is_authenticated()
	
	@expose('/')
	def index(self):
		login.logout_user()
		self.admin.menu()[0].name = 'Home'
		return redirect(url_for('admin.index'))

class LoginView(AdminIndexView):
    	def is_accessible(self):
        	return not login.current_user.is_authenticated()

	@expose('/', methods=('GET', 'POST'))
	def index(self):
		form = LoginForm(request.form)
		if form.validate_on_submit():
			user = form.get_user()
			login.login_user(user)
			self.admin.menu()[0].name = user.login
			return self.render('welcome.html')

		return self.render('login_form.html', form=form)


# Create customized model view class
class MyModelView(sqlamodel.ModelView):
	def is_accessible(self):
		return login.current_user.is_authenticated()
	
#for testing
'''
class RaceView(sqlamodel.ModelView):
	def is_accessible(self):
		return login.current_user.is_authenticated()

	inline_models = (Highlight,)

class HighlightView(sqlamodel.ModelView):
	def is_accessible(self):
		return login.current_user.is_authenticated()
'''
