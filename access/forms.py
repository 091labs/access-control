from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required, EqualTo


class LoginForm(Form):
    email = TextField('email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class NewAdminForm(Form):
    password = PasswordField('password', validators=[
        Required(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirm_password', validators=[Required()])
