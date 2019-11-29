"""
Forms with validators for these forms
"""
from enum import Enum
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


class RegistrationForm(FlaskForm):
    """
    Registration form
    """
    username = StringField("Username", validators=[DataRequired(), check_user_in_db_reg])
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired(), check_password])
    password_repeat = PasswordField("Password Repeat")
    submit = SubmitField()


def project_choices():
    projects = services.projects.get_projects()
    return [(project.id, project.title) for project in projects]


def create_note_form(**kwargs) -> 'NoteForm':
    """
    Create Note Form
    :param kwargs:
    :return: Note form or Note form with data
    """
    projects = services.projects.get_projects_for_form(session['user_id'])

    form: NoteForm = NoteForm()
    form.set_choices(projects)

    if 'description' in kwargs:
        form.description.data = kwargs['description']
    if 'status' in kwargs:
        form.status.data = kwargs['status']
    if 'project' in kwargs:
        form.project.data = kwargs['project']

    return form


class Statuses(Enum):
    OPEN = 'Open'
    CLOSED = 'Closed'
    IN_PROGRESS = 'In Progress'
    RESOLVED = 'Resolved'


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
    project = SelectField("Project", coerce=int, choices=project_choices())
    submit = SubmitField()

    def set_choices(self, projects):
        self.project.choices = [(project.id, project.title) for project in projects]

    def serialize(self):
        return {
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'submit': self.submit
        }


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
    Note form
    """
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[])
    submit = SubmitField()
