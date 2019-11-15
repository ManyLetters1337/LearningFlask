from flask import Flask, flash, url_for, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from model.models import User, Note
from form.forms import LoginForm, RegistrationForm, AddNoteForm
from database import DataBase
import logging
import os

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://manyletters:12345678*Aa@localhost/base'

db = SQLAlchemy(app)
login_manager = LoginManager(app)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

database = DataBase()


@app.route('/', methods=['POST', 'GET'])
def index_page():
    if 'user_id' in session:
        return render_template("index_page.html", notes=database.get_notes_for_user(session['user_id']))
    else:
        return render_template("index_page.html")


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        database.login_user(form.username.data, form.remember.data)
        return redirect(url_for('index_page'))
    return render_template('login.html', form=form)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        database.add_user(form.username.data, form.email.data, form.password.data)
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))


@app.route('/add_note', methods=['POST', 'GET'])
def add_note():
    form = AddNoteForm()
    if form.validate_on_submit():
        database.add_note(form.title.data, form.description.data, session['user_id'])
        return redirect(url_for('index_page'))
    return render_template('add_note.html', form=form)


if __name__ == '__main__':
    app.run();
