from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Handle requests to register url
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, name=form.name.data, password=form.password.data)
        #add user to database
        db.session.add(user)
        db.session.commit()
        flash('The user have been created successfully!')

        # redirect to login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Handle requests to login url
    form = LoginForm()
    if form.validate_on_submit():
        #check if user exists in database and password matches
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            # log the user in
            login_user(user)

            # redirect to the dashboard page
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        # if login is incorrect
        else:
            flash('Username or password is not correct!')

    # Load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    # Handle requests to logout url
    logout_user()
    flash('You have been logged out successfully!')

    # redirect to the login page
    return redirect(url_for('auth.login'))

