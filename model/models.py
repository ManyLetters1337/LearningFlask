from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    user_uuid = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String(70), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)

    def set_uuid(self, user_uuid):
        self.user_uuid = user_uuid

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer(), primary_key=True)
    note_uuid = db.Column(db.String(), nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(511), nullable=True)
    status = db.Column(db.Boolean())
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def set_created(self):
        self.created_on = datetime.now()

    def set_uuid(self, note_uuid):
        self.note_uuid = note_uuid

    def set_user(self, user_id):
        self.user_id = user_id
