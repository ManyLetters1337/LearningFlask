"""
Forms with validators for these forms
"""
from config import Statuses
from flask import flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, SelectField
from werkzeug.security import check_password_hash
from wtforms.validators import DataRequired, Email, ValidationError
from database.service_registry import services


def check_user_in_db_log(form, field):
    """
    Checking the presence of a user in the database
    :param form:
    :param field:
    :return: ValidationError or None
    """
    message = "Wrong username"
    if not services.users.get_user_by_name(field.data):
        flash(message)
        raise ValidationError(message)


def check_user_password(form, field):
    """
    Check user password
    :param form:
    :param field:
    :return: ValidationError or None
    """
    if services.users.get_user_by_name(form.username.data):
        message = "Wrong Password"
        if not check_password_hash(services.users.get_password_hash(form.username.data), field.data):
            flash(message)
            raise ValidationError(message)


def create_login_form():
    """
    Create log in form
    :return:
    """
    form: LoginForm = LoginForm()

    return form


class LoginForm(FlaskForm):
    """
    Log in form
    """
    username = StringField("Username", validators=[DataRequired(), check_user_in_db_log])
    password = PasswordField("Password", validators=[DataRequired(), check_user_password])
    remember = BooleanField("Remember me")
    submit = SubmitField()


def check_password(form, field):
    """
    Check for password matches
    :param form:
    :param field:
    :return: ValidationError or None
    """
    message = "Passwords do not match"
    if not form.password.data == form.password_repeat.data:
        flash(message)
        raise ValidationError(message)


def check_user_in_db_reg(form, field):
    """
    Checking the presence of a user in the database
    :param form:
    :param field:
    :return: ValidationError or None
    """
    message = "User already exist"
    if services.users.get_user_by_name(field.data):
        flash(message)
        raise ValidationError(message)


def check_email_in_db(form, field):
    """
    Checking the presence of a user in the database
    @param form:
    @param field:
    @return:
    """
    message = "User with this email already exist"
    if services.users.get_user_by_email(field.data):
        flash(message)
        raise ValidationError(message)


def create_registration_form():
    """
    Create registration form
    :return:
    """
    form: RegistrationForm = RegistrationForm()

    return form


class RegistrationForm(FlaskForm):
    """
    Registration form
    """
    username = StringField("Username", validators=[DataRequired(), check_user_in_db_reg])
    email = StringField("Email", validators=[Email(), check_email_in_db])
    password = PasswordField("Password", validators=[DataRequired(), check_password])
    password_repeat = PasswordField("Password Repeat")
    submit = SubmitField()


def create_note_form(user_id: id, **kwargs) -> 'NoteForm':
    """
    Create Note Form
    :param kwargs:
    :return: Note form or Note form with data
    @param user_id:
    """
    user = services.users.get_by_id(session['user_id'])
    form: NoteForm = NoteForm()

    projects = services.projects.get_projects(user)
    form.project.choices = [(project.id, project.title) for project in projects]

    users = services.users.get_all()
    form.user.choices = [(user.id, user.username) for user in users]
    form.user.data = user_id

    if 'description' in kwargs:
        form.description.data = kwargs['description']
    if 'status' in kwargs:
        form.status.data = kwargs['status']
    if 'project' in kwargs:
        form.project.data = kwargs['project']

    return form


class NoteForm(FlaskForm):
    """
    Note form
    """
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[])
    status = SelectField("Status", choices=[(Statuses.OPEN.value, Statuses.OPEN.value),
                                            (Statuses.IN_PROGRESS.value, Statuses.IN_PROGRESS.value),
                                            (Statuses.RESOLVED.value, Statuses.RESOLVED.value),
                                            (Statuses.CLOSED.value, Statuses.CLOSED.value)], validators=[]
                         )
    project = SelectField("Project", coerce=int)
    user = SelectField("User", coerce=int)
    submit = SubmitField()


def create_project_form(**kwargs) -> 'ProjectForm':
    """
    Create Note Form
    :param kwargs:
    :return: Note form or Note form with data
    """

    form: ProjectForm = ProjectForm()

    if 'description' in kwargs:
        form.description.data = kwargs['description']

    return form


class ProjectForm(FlaskForm):
    """
    Зкщоусе form
    """
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[])
    submit = SubmitField()

