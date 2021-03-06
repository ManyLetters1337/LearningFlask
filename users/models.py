"""
User Class
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from database.core import db
from time import time
from config import secret_key
import jwt
import uuid


association_table = db.Table('notes_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id'))
)


class User(db.Model, UserMixin):
    """
    Model of User
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(50), default=uuid.uuid4().__str__(), unique=True)
    username = db.Column(db.String(70), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    projects = db.relationship('Project', backref='user', lazy=True)
    note = db.relationship('Note', secondary=association_table, back_populates="user")

    def set_uuid(self, uuid_: str):
        """
        Set user uuid
        :param uuid_:
        """
        self.uuid = uuid_

    def set_password(self, password: str):
        """
        Set user password_hash
        :param password:
        """
        self.password_hash = generate_password_hash(password)

    def get_reset_password_token(self, expire_in=600):
        """
        Get Reset Password Token for User
        @param expire_in:
        @return:
        """
        return jwt.encode({'reset_password': self.id, 'exp': time() + expire_in},
                          secret_key, algorithm='HS256').decode('utf-8')

    def serialize(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'username': self.username,
            'email': self.email,
        }

