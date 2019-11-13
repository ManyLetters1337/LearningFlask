from flask import Flask, flash, url_for, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from models import User, Note
from forms import LoginForm, RegistrationForm, AddNoteForm
from datetime import datetime


import os

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Many_Letters:VitaLol1337@localhost/testDB'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@app.route('/')
def index_page():
	if 'username' in session:
		return render_template("index_page.html", username = session['username'])
	else:
		return render_template("index_page.html") 



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@app.route('/login', methods = ['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.query(User).filter(User.username == form.username.data).first()
		if user and user.check_password(form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('index_page'))
		flash("Invalid username/password", 'error')
		return redirect(url_for('login'))
	return render_template('login.html', form=form)

@app.route('/registration', methods = ['POST', 'GET'])
def registration():
	form = RegistrationForm()
	if form.validate_on_submit():
		if not db.session.query(User).filter(User.username == form.username.data).first():
			if form.check_password:
				user = User(username = form.username.data, email = form.email.data)
				user.set_password(form.password.data)
				db.session.add(user)
				db.session.commit()
				session['user_id'] = db.session.query(User).filter(User.username == user.username).first().id
				return redirect(url_for('login'))
			flash("Invalid password repeat", 'error')
		flash("User already exist", 'error')
		return redirect(url_for('registration'))
	return render_template('registration.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/add_note', methods = ['POST', 'GET'])
def add_note():
	form = AddNoteForm()
	if form.validate_on_submit():
		note = Note(title = form.title.data, description = form.description.data, status = False)
		note.set_created()
		db.session.add(note)
		db.session.commit()
		return redirect(url_for('index_page'))
	return render_template('add_note.html', form=form)	

if __name__ == '__main__':
	app.run();