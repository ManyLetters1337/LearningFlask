"""
User Class
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from database.core import db
import uuid


class User(db.Model, UserMixin):
    """
    Model of User
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String(70), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)

    def set_uuid(self, uuid_: str) -> db.Model:
        """
        Set user uuid
        :param uuid_:
        """
        self.uuid = uuid_

    def set_password(self, password: str) -> db.Model:
        """
        Set user password_hash
        :param password:
        """
        self.password_hash = generate_password_hash(password)

    def serialize(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash
        }

