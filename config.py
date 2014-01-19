import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://root:changeme@localhost/users'

CSRF_ENABLED = True
SECRET_KEY = 'changeme'
