"""
Project Class
"""
from database.core import db
from datetime import datetime
import uuid


class Project(db.Model):
    """
    Model of Project
    """
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(50), default=uuid.uuid4().__str__(), unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    notes = db.relationship('Note', backref='project', lazy=True)

    def set_uuid(self, uuid_):
        """
        Set project uuid
        :param uuid_:
        """
        self.uuid = uuid_

    def set_user(self, user):
        """
        Set user_id in project
        :param id_:
        """
        self.user = user

    def serialize(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'created_on': self.created_on
        }
