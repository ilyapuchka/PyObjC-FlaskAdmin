from flask import Flask
from os import path
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from views import *
from documents import *
from ModelGenerator import *

modelGenerator = ModelGenerator(app, db)

init_login()
admin = Admin(app, name = 'Admin', index_view=LoginView(name='Login', category='Home'))
admin.add_view(LoggedUserIndexView(name='Home', endpoint='home', category='Home'))
admin.add_view(LogoutView(name='Logout', endpoint='logout', category='Home'))

	
for key, tupple in  modelGenerator.compile().items():
	admin.add_view(tupple[1](tupple[0], db.session))

'''

admin.add_view(RaceView(Race, db.session))
admin.add_view(HighlightView(Highlight, db.session))
'''

db.create_all()

