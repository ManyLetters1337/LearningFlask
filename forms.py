from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,  BooleanField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember me")
	submit = SubmitField()


class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	email = StringField("Email", validators=[Email()])
	password = PasswordField("Password", validators=[DataRequired()])
	password_repeat = PasswordField("Password Repeat", validators=[DataRequired()])
	submit = SubmitField()

	def check_password(self):
		return self.password == self.password_repeat

