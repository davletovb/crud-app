from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from app import db, login_manager


class User(UserMixin, db.Model):
    # User table

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    name = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        # Protect the password from reading
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        # Set a hashed password
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # Check if password matches the hashed password
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Load user with user id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    # Role table

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class UserAccount(db.Model):
    # UserAccount table for STIX format

    __tablename__ = 'user_accounts'

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(64), default="user-account")
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    modified = db.Column(db.DateTime, default=datetime.datetime.now)
    account_type = db.Column(db.String(32), nullable=True)
    account_created = db.Column(db.DateTime, nullable=True)
    account_is_disabled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User Account: {}>'.format(self.name)


class Identity(db.Model):
    # Identity table for STIX format

    __tablename__ = 'identities'

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(64), default="identity")
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    modified = db.Column(db.DateTime, default=datetime.datetime.now)
    identity_role = db.Column(db.Integer, db.ForeignKey('identityroles.id', ondelete=db.null), nullable=True)
    identity_class = db.Column(db.Integer, db.ForeignKey('identityclasses.id', ondelete=db.null), nullable=True)
    contact_information = db.Column(db.String(128), nullable=True)
    location = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return '<Identity: {}>'.format(self.name)


class ThreatActor(db.Model):
    # Threat Actor table for STIX format

    __tablename__ = 'threat_actors'

    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(64), default="threat-actor")
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    modified = db.Column(db.DateTime, default=datetime.datetime.now)
    threat_actor_types = db.Column(db.Integer, db.ForeignKey('threatactortypes.id', ondelete=db.null), nullable=True)
    aliases = db.Column(db.String(64), nullable=True)
    first_seen = db.Column(db.DateTime, default=datetime.datetime.now)
    last_seen = db.Column(db.DateTime, default=datetime.datetime.now)
    threat_actor_roles = db.Column(db.Integer, db.ForeignKey('threatactorroles.id', ondelete=db.null), nullable=True)
    goals = db.Column(db.String(64), nullable=True)
    sophistication = db.Column(db.Integer, db.ForeignKey('threatactorsophistications.id', ondelete=db.null), nullable=True)
    resource_level = db.Column(db.Integer, db.ForeignKey('attackresourcelevels.id', ondelete=db.null), nullable=True)
    primary_motivation = db.Column(db.Integer, db.ForeignKey('attackmotivations.id', ondelete=db.null), nullable=True)
    secondary_motivations = db.Column(db.Integer, db.ForeignKey('attackmotivations.id', ondelete=db.null), nullable=True)
    personal_motivations = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return '<Threat Actor: {}>'.format(self.name)


class Post(db.Model):
    # UserAccount table for STIX format

    __tablename__ = 'posts'

    id = db.Column(db.String(64), primary_key=True)
    text = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(64), default="post")
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    modified = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Post: {}>'.format(self.text)


class ThreatActorSophistication(db.Model):
    # Threat Actor Sophistication OV table

    __tablename__ = 'threatactorsophistications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)


class AttackResourceLevel(db.Model):
    # Attack Resource Level OV table

    __tablename__ = 'attackresourcelevels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)


class AttackMotivation(db.Model):
    # Attack Motivation OV table

    __tablename__ = 'attackmotivations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)


class ThreatActorType(db.Model):
    # Threat Actor Type OV table

    __tablename__ = 'threatactortypes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)


class ThreatActorRole(db.Model):
    # Threat Actor Role OV table

    __tablename__ = 'threatactorroles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)


class IdentityClass(db.Model):
    # Identity Class OV table

    __tablename__ = 'identityclasses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)


class IdentityRole(db.Model):
    # Identity Role OV table

    __tablename__ = 'identityroles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=True)