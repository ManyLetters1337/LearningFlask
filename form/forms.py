"""
Forms with validators for these forms
"""
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, SelectField
from werkzeug.security import check_password_hash
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
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


class NoteForm(FlaskForm):
    """
    Note form
    """
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[])
    status = SelectField("Status", choices=[("Open", "Open"), ("In Progress", "In Progress"),
                                            ("Resolved", "Resolved"), ("Closed", "Closed")], validators=[])
    project = SelectField("Project", coerce=int, choices=project_choices())
    submit = SubmitField()


class ProjectForm(FlaskForm):
    """
    Note form
    """
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[])
    submit = SubmitField()
