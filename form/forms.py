from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField
from werkzeug.security import check_password_hash
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from database import DataBase

dbclass = DataBase()


def check_user_in_db_log(form, field):
    message = "Wrong username"
    if not dbclass.get_user_by_name(field.data):
        flash(message)
        raise ValidationError(message)


def check_user_password(form, field):
    if dbclass.get_user_by_name(form.username.data):
        message = "Wrong Password"
        if not check_password_hash(dbclass.get_password_hash(form.username.data), field.data):
            flash(message)
            raise ValidationError(message)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), check_user_in_db_log])
    password = PasswordField("Password", validators=[DataRequired(), check_user_password])
    remember = BooleanField("Remember me")
    submit = SubmitField()


def check_password(form, field):
    message = "Passwords do not match"
    if not form.password.data == form.password_repeat.data:
        flash(message)
        raise ValidationError(message)


def check_user_in_db_reg(form, field):
    message = "User already exist"
    if dbclass.get_user_by_name(field.data):
        flash(message)
        raise ValidationError(message)


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), check_user_in_db_reg])
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired(), check_password])
    password_repeat = PasswordField("Password Repeat")
    submit = SubmitField()


class AddNoteForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField()
