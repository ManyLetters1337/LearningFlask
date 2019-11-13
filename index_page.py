from flask import Flask, flash, url_for, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, current_user
from models import User, Note
from forms import LoginForm


import os

app = Flask(__name__)
app.debug = False
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Many_Letters:VitaLol1337@localhost/testDB'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@app.route('/')
def index_page():
	if 'username' in session:
		return render_template("index_page.html", username = session['username'])
	else:
		return render_template("index_page.html") 

@app.route('/login', methods = ['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.query(User).filter(User.username == form.username.data).first()
		if user and user.check_password(form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('admin'))
		return redirect(url_for('login'))
	return render_template('login.html', form=form)



@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index_page'))


if __name__ == '__main__':
	app.run();