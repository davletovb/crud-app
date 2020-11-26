from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError

from ..models import UserAccount, Identity, ThreatActor, ThreatActorSophistication, ThreatActorRole, ThreatActorType, \
    AttackResourceLevel, AttackMotivation, IdentityClass, IdentityRole


class UserAccountForm(FlaskForm):
    # Form to create a new user account

    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    account_type = StringField('Account type')
    account_created = DateField('Account created')
    account_is_disabled = BooleanField('Account is disabled')
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if UserAccount.query.filter_by(name=field.data).first():
            raise ValidationError('Name is already in use!')


class UserAccountEditForm(FlaskForm):
    # Form to edit an user account

    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    account_type = StringField('Account type')
    account_created = DateField('Account created')
    account_is_disabled = BooleanField('Account is disabled')
    submit = SubmitField('Submit')


class IdentityForm(FlaskForm):
    # Form to create a new identity

    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    contact_information = StringField('Contact information')
    location = StringField('Location')
    identity_role = QuerySelectField(query_factory=lambda: IdentityRole.query.all(), get_label='name')
    identity_class = QuerySelectField(query_factory=lambda: IdentityClass.query.all(), get_label='name')
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if Identity.query.filter_by(name=field.data).first():
            raise ValidationError('Name is already in use!')


class ThreatActorForm(FlaskForm):
    # Form to create a new threat actor

    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    contact_information = StringField('Contact information')
    aliases = StringField('Aliases')
    first_seen = DateField('First seen')
    last_seen = DateField('Last seen')
    goals = StringField('Goals')
    threat_actor_type = QuerySelectField(query_factory=lambda: ThreatActorType.query.all(), get_label='name')
    threat_actor_role = QuerySelectField(query_factory=lambda: ThreatActorRole.query.all(), get_label='name')
    threat_actor_sophistication = QuerySelectField(query_factory=lambda: ThreatActorSophistication.query.all(),
                                                   get_label='name')
    resource_level = QuerySelectField(query_factory=lambda: AttackResourceLevel.query.all(), get_label='name')
    primary_motivation = QuerySelectField(query_factory=lambda: AttackMotivation.query.all(), get_label='name')
    secondary_motivation = QuerySelectField(query_factory=lambda: AttackMotivation.query.all(), get_label='name')
    personal_motivations = StringField('Personal motivations')
    submit = SubmitField('Submit')

    def validate_name(self, field):
        if ThreatActor.query.filter_by(name=field.data).first():
            raise ValidationError('Name is already in use!')


class PostForm(FlaskForm):
    # Form to create a new post

    text = StringField('Name')
    description = StringField('Description')
    submit = SubmitField('Submit')


class ThreatActorSophisticationForm(FlaskForm):
    # Form to add threat actor sophistications
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class AttackResourceLevelForm(FlaskForm):
    # Form to add attack resource level
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class AttackMotivationForm(FlaskForm):
    # Form to add attack motivation
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class ThreatActorTypeForm(FlaskForm):
    # Form to add threat actor type
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class ThreatActorRoleForm(FlaskForm):
    # Form to add threat actor role
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class IdentityClassForm(FlaskForm):
    # Form to add identity class
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class IdentityRoleForm(FlaskForm):
    # Form to add identity role
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')
