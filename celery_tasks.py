from flask import Flask, render_template
from celery import Celery
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'some-login-post@yandex.ru'
app.config['MAIL_PASSWORD'] = 'Qwerty123'
app.config['MAIL_DEFAULT_SENDER'] = 'some-login-post@yandex.ru'

mail = Mail(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task()
def send_mail(username: str, email: str):
    with app.app_context():
        msg = Message("Hello User", recipients=[email])
        msg.html = render_template('mail_assign_user.html', username=username)
        mail.send(msg)


@celery.task()
def send_assign_mail(username: str, email: str, url: str):
    with app.app_context():
        msg = Message("Hello User", recipients=[email])
        msg.html = render_template('mail_assign_user.html', username=username, url=url)
        mail.send(msg)


@celery.task()
def send_reset_password_email(username: str, email: str, url: str):
    with app.app_context():
        msg = Message("Reset Password", recipients=[email])
        msg.html = render_template('mail_reset_password.html', username=username, url=url)
        mail.send(msg)
