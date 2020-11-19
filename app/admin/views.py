from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import UserForm, UserEditForm, RoleForm
from .. import db
from ..models import User, Role


def check_admin():
    # Allow only admins to access the page
    if not current_user.is_admin:
        abort(403)


# User views
@admin.route('/users')
@login_required
def list_users():
    # List all users
    users = User.query.all()
    return render_template('admin/users/users.html', users=users, title='Users')


@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    # Handle requests to add user url
    # Edit a user
    check_admin()

    add_user = True

    form = UserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, name=form.name.data,
                    role=form.role.data, password=form.password.data, is_admin=form.is_admin.data)
        # add user to database
        db.session.add(user)
        db.session.commit()
        flash('The user have been created successfully!')

        # redirect to login page
        return redirect(url_for('admin.list_users'))

    # load registration template
    return render_template('admin/users/user.html', add_user=add_user, form=form, title='Add user')


@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    # Edit a user
    check_admin()

    add_user = False

    user = User.query.get_or_404(id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.name = form.name.data
        #user.password = form.password.data
        user.role = form.role.data
        user.is_admin = form.is_admin.data
        db.session.add(user)
        db.session.commit()
        flash('The user has been edited successfully!')

        # redirect to the users page
        return redirect(url_for('admin.list_users'))

    form.email.data = user.email
    form.username.data = user.username
    form.name.data = user.name
    #form.password.data = user.password
    form.is_admin.data = user.is_admin
    return render_template('admin/users/user.html', add_user=add_user, form=form, title='Edit user')


# Role views
@admin.route('/roles')
@login_required
def list_roles():
    # List all roles
    roles = Role.query.all()
    return render_template('admin/roles/roles.html', roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    # Create a new role
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data, description=form.description.data)

        try:
            # add the new role to database
            db.session.add(role)
            db.session.commit()
            flash('The new role has been added successfully!')
        except:
            # if the role already exist
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role, form=form, title='Add role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    # Edit a role
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('The role has been edited successfully!')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role, form=form, title='Edit role')


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    # Delete a role
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('The role has been deleted successfully!')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title='Delete role')
