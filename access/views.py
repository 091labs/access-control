from access import login_manager, app
from access.forms import LoginForm
from access.models import User

from flask import g, redirect, url_for, render_template, request, flash
from flask.ext.login import login_required, current_user, login_user, logout_user

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user=user, remember=form.remember_me.data)
                flash('Logged in as %s' % user.email)
                return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
