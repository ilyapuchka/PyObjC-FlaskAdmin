import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'e\xd7~>\xa6+\x0f\x1a\x80\xbb\xc6\x1d\xfb\xed]\x89\x87V\x99R\x04\x94e<'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'Admin.db')
SQLALCHEMY_ECHO = True

MODEL_URI = './test/Model.xcdatamodeld'
MOM_URI = '~/Documents/Python\ projects/Admin/Model.mom'

