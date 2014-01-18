import hashlib
import uuid

from access import db
from access.constants import ROLE_USER, ROLE_ADMIN

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    key_id = db.Column(db.Integer)
    pw_hash = db.Column(db.String(128))
    pw_salt = db.Column(db.String(32))

    def __init__(self, name, email, key_id):
        self.name = name
        self.email = email
        self.key_id = key_id

    def make_admin(self, password):
        self.role = ROLE_ADMIN
        self.pw_salt = uuid.uuid4().hex
        self.pw_hash = hashlib.sha512(password + self.pw_salt).hexdigest()

    def make_user(self):
        self.role = ROLE_USER
        self.pw_salt = None
        self.pw_hash = None

    def check_password(self, password):
        if self.role != ROLE_ADMIN:
            return False
        check_hash = hashlib.sha512(password + self.pw_salt).hexdigest()
        return check_hash == self.pw_hash

    def is_authenticated(self):
        return True

    def is_active(self):
        """
        We're only allowing admins to login, that is only
        admins will be considered active.
        """
        return self.role == ROLE_ADMIN

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)
