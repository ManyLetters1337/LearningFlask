from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Many_Letters:VitaLol1337@localhost/testDB'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

class User(db.Model, UserMixin):
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