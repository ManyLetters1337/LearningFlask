"""
Authentication views for User Class
"""
from typing import TYPE_CHECKING
from flask import flash, url_for, render_template, redirect, request, Blueprint
from create_app import login_manager
from form.forms import create_login_form, create_registration_form, ResetPasswordRequest, ResetPassword
from database.service_registry import services
from flask_login import login_required, logout_user, login_user
from celery_tasks import send_mail, send_reset_password_email

if TYPE_CHECKING:
    from users.models import User
    from form.forms import LoginForm
    from form.forms import RegistrationForm

login_manager.login_view = 'auth.login'

auth = Blueprint('auth', __name__, template_folder='templates/auth')


@login_manager.user_loader
def load_user(user_id: int) -> 'User':
    """
    Load current logged-in user
    :param user_id: int (User.id)
    :return: User instance
    """
    return services.users.get_by_id(user_id)


@auth.route('/login', methods=['GET'])
def login():
    """
    Get method for log in page
    :return: Page with Log In form or page with notes for logged-in user
    """
    form: 'LoginForm' = create_login_form()

    return render_template('login.html', form=form)


@auth.route('/login', methods=['POST'])
def login_post():
    """
    Post method for log in page
    :return: Page with Log In form or page with notes for logged-in user
    """
    form: 'LoginForm' = create_login_form()
    if form.validate():
        login_user(services.users.get_by_id(services.users.get_id_by_name(form.username.data)),
                   remember=form.remember.data)
        return redirect(request.args.get('next') or url_for('notes.notes_page'))
    return render_template('login.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET'])
def reset_password(token):
    """
    Page With Reset Password Form
    @return:
    """
    form: ResetPassword = ResetPassword()

    return render_template('reset_password.html', form=form)


@auth.route('/reset_password/<token>', methods=['POST'])
def reset_password_post(token):
    """
    Reset Password
    @return:
    """
    form: ResetPassword = ResetPassword()

    if form.validate():
        user: 'User' = services.users.verify_reset_password_token(token)
        user = services.users.reset_password(form.password.data)

        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


@auth.route('/reset_password_request', methods=['GET'])
def reset_password_request():
    """
    Page with Reset Password Request Form
    @return:
    """
    form: ResetPasswordRequest = ResetPasswordRequest()

    return render_template('reset_password_request.html', form=form)


@auth.route('/reset_password_request', methods=['POST'])
def reset_password_request_post():
    """
    Page with Reset Password Request Form Post
    @return:
    """
    form: ResetPasswordRequest = ResetPasswordRequest()

    if form.validate():
        user: User = services.users.get_user_by_email(form.email.data)
        token = user.get_reset_password_token()
        url = url_for('auth.reset_password', token=token, _external=True)
        send_reset_password_email.apply_async(args=[user.username, user.email, url])

        flash("Check Your Email")
        return redirect(url_for('auth.login'))

    return render_template('reset_password_request.html', form=form)


@auth.route('/registration', methods=['GET'])
def registration():
    """
    Get method for registration page
    :return: Page with registration form or page with notes for registered user
    """
    form: 'RegistrationForm' = create_registration_form()

    return render_template('registration.html', form=form)


@auth.route('/registration', methods=['POST'])
def registration_post():
    """
    Post method for registration page
    :return: Page with registration form or page with notes for registered user
    """
    form: 'RegistrationForm' = create_registration_form()

    if form.validate_on_submit():
        user: 'User' = services.users.create(form.username.data, form.email.data, form.password.data)
        send_mail.apply_async(args=[user.username, user.email])
        return redirect(request.args.get('next') or url_for('notes.notes_page'))

    return render_template('registration.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """
    User log out
    :return: Page with Log In form
    """
    logout_user()
    flash("You have been logged out.")

    return redirect(url_for('auth.login'))
