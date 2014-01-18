from access import login_manager, app, db
from access.constants import *
from access.forms import LoginForm, NewAdminForm
from access.models import User

from flask import g, redirect, url_for, render_template, request, flash, abort
from flask.ext.login import login_required, current_user
from flask.ext.login import login_user, logout_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.context_processor
def inject_constants():
    # this disgusts me... but it works
    return {
        'ROLE_USER': ROLE_USER,
        'ROLE_ADMIN': ROLE_ADMIN
    }


@app.route('/')
@app.route('/index')
@login_required
def index():
    return redirect(url_for('users'))


@app.route('/users')
@login_required
def users():
    return render_template('users.html', title='Users', users=User.query.all())


@app.route('/users/make_admin/<int:id>', methods=['GET', 'POST'])
@login_required
def make_admin(id):
    form = NewAdminForm()
    user = User.query.get(id)
    if not user:
        abort(404)
    if form.validate_on_submit():
        if user:
            user.make_admin(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('%s is now an admin' % user.email, 'success')
            return redirect(url_for('users'))
    return render_template('new_admin.html', user=user, form=form)


@app.route('/user/make_user/<int:id>')
@login_required
def make_user(id):
    user = User.query.get(id)
    if user:
        user.make_user()
        db.session.add(user)
        db.session.commit()
        flash('%s is no longer an admin' % user.email, 'info')
    return redirect(url_for('users'))


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
                flash('Logged in as %s' % user.email, 'success')
                return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('index'))
