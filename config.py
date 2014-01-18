import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'users.db')

CSRF_ENABLED = True
SECRET_KEY = '69fe28e5-4dba-4752-abf4-8be4fd2f18a1'
