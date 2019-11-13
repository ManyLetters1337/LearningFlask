from flask import Flask, flash, url_for, session, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.debug = False
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Many_Letters:VitaLol1337@localhost/testDB'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(70), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    notes = db.relationship('Note', backref='user')

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password)

    def check_password(self, password):
    	return check_password_hash(self.password_hash, password)


class Note(db.Model):
	__tablename__ = 'notes'
	id = db.Column(db.Integer(), primary_key = True)
	user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
	title = db.Column(db.String(255), nullable = False)
	description = db.Column(db.String(511), nullable = True)
	created_on = db.Column(db.DateTime(), default=datetime.utcnow)


@app.route('/')
def index_page():
	if 'username' in session:
		return render_template("index_page.html", username = session['username'])
	else:
		return render_template("index_page.html") 

@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		user = User(username = request.form['username'], email = request.form['email'], password_hash = generate_password_hash(request.form['password']))
		db.session.add(user)
		db.session.commit()
		flash("You were successfully logged in")
		return redirect(url_for('index_page'))
	else:
		return render_template('login.html')



@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('index_page'))


if __name__ == '__main__':
	app.run();