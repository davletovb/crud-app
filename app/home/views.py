from flask import abort, render_template
from flask_login import current_user, login_required

from . import home


@home.route('/')
def homepage():
    # handle the request to home page
    return render_template('home/index.html', title="Home page")


@home.route('/dashboard')
@login_required
def dashboard():
    # handle the request to dashboard url
    return render_template('home/dashboard.html', title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # only admins will access this page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Admin Dashboard")
