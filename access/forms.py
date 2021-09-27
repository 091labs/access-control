from flask_wtf import Form
from wtforms.fields import TextField, BooleanField, PasswordField
from wtforms.validators import Required, EqualTo


class LoginForm(Form):
    email = TextField('email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class NewPasswordForm(Form):
    password = PasswordField('password', validators=[
        Required(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('confirm_password', validators=[Required()])


class NewKeyForm(Form):
    key_id = TextField('key_id', validators=[Required()])


class NewUserForm(Form):
    name = TextField('name', validators=[Required()])
    email = TextField('email', validators=[Required()])
    key_id = TextField('key_id', validators=[Required()])
