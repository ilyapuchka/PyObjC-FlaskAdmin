from myadmin import db
from flask.ext import wtf
from myadmin.documents import User


class LoginForm(wtf.Form):
    login = wtf.TextField('Login:', validators=[wtf.required()])
    password = wtf.PasswordField('Password:', validators=[wtf.required()])

    def validate_login(self, field):

        user = self.get_user()

        if user is None:
            raise wtf.ValidationError('Invalid user')

        if user.password != self.password.data:
            raise wtf.ValidationError('Invalid password')

    def get_user(self):
	print 'get_user login %s' % self.login.data
        return db.session.query(User).filter_by(login=self.login.data).first()

