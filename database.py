from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from model.models import User, Note
import uuid

app = Flask(__name__)
db = SQLAlchemy(app)

class DataBase:
    def add_user(self, username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        user_uuid = uuid.uuid1().__str__()
        user.set_uuid(user_uuid)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = self.get_id_by_name(username)

    def get_user_by_name(self, username):
        return db.session.query(User).filter(User.username == username).first()

    def get_user_by_id(self, id):
        return db.session.query(User).filter(User.id == id).first()

    def get_password_hash(self, username):
        return db.session.query(User).filter(User.username == username).first().password_hash


    def get_id_by_name(self, username):
        return db.session.query(User).filter(User.username == username).first().id

    def login_user(self, username, remember):
        user = self.get_user_by_name(username)
        login_user(user, remember=remember)

    def get_notes(self):
        return db.session.query(Note).all()