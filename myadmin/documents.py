from myadmin import db
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin.contrib import sqlamodel

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

#for testing
'''
class Race(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	videoURL = db.Column(db.String(80), nullable=False)
	#one-to-many relationship
	#race can have many highlights
	highlights = db.relationship('Highlight', backref='race')

	def __unicode__(self):
		return self.title

class Highlight(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	videoURL = db.Column(db.String(80), nullable=False)
	#one-to-many relationship
	#highligh can have only one race
	race_id = db.Column(db.Integer(), db.ForeignKey('race.id'), nullable=False)
		
	def __unicode__(self):
		return self.title
'''	
	

