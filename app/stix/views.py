from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import stix
from .forms import UserAccountForm, UserAccountEditForm, IdentityForm, ThreatActorForm, PostForm, ThreatActorSophisticationForm, AttackResourceLevelForm, AttackMotivationForm, ThreatActorTypeForm, ThreatActorRoleForm, IdentityClassForm, IdentityRoleForm
from .. import db
from ..models import UserAccount, Identity, ThreatActor, Post, ThreatActorSophistication, AttackResourceLevel, AttackMotivation, ThreatActorType, ThreatActorRole, IdentityClass, IdentityRole


def check_user():
    # Allow only users with assigned roles to access the page
    if not current_user.is_admin:
        abort(403)


# User views
@stix.route('/user-accounts')
@login_required
def list_user_accounts():
    # List all users
    user_accounts = UserAccount.query.all()
    return render_template('admin/users/users.html', users=user_accounts, title='User Accounts')


@stix.route('/user-accounts/add', methods=['GET', 'POST'])
@login_required
def add_user_account():
    # Handle requests to add user url
    # Edit a user
    check_user()

    add_user = True

    form = UserAccountForm()
    if form.validate_on_submit():
        user_account = UserAccount(name=form.name.data,
                    description=form.description.data, account_type=form.account_type.data, account_created=form.account_created.data, account_is_disabled=form.account_is_disabled.data)
        # add user to database
        db.session.add(user_account)
        db.session.commit()
        flash('The user account have been created successfully!')

        # redirect to list accounts
        return redirect(url_for('stix.list_user_accounts'))

    # load registration template
    return render_template('admin/users/user.html', add_user=add_user, form=form, title='Add user')


@stix.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    # Edit a user
    check_user()

    add_user = False

    user = UserAccount.query.get_or_404(id)
    form = UserAccountEditForm(obj=user)
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
@stix.route('/roles')
@login_required
def list_roles():
    # List all roles
    roles = IdentityRole.query.all()
    return render_template('admin/roles/roles.html', roles=roles, title='Roles')


@stix.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    # Create a new role
    check_user()

    add_role = True

    form = IdentityRoleForm()
    if form.validate_on_submit():
        role = IdentityRole(name=form.name.data, description=form.description.data)

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


@stix.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    # Edit a role
    check_user()

    add_role = False

    role = IdentityRole.query.get_or_404(id)
    form = IdentityRoleForm(obj=role)
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


@stix.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    # Delete a role
    check_user()

    role = IdentityRole.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('The role has been deleted successfully!')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title='Delete role')
