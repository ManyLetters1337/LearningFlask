"""
Note Class
"""
from database.core import db
from datetime import datetime
import uuid


class Note(db.Model):
    """
    Model of Note
    """
    __tablename__ = 'notes'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    def set_uuid(self, uuid_):
        """
        Set note uuid
        :param uuid_:
        """
        self.uuid = uuid_

    def set_project(self, id_):
        """
        Set project in note
        :param id_:
        :return:
        """
        self.project_id = id_

    def set_user(self, id_):
        """
        Set user_id in note
        :param id_:
        """
        self.user_id = id_

    def serialize(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_on': self.created_on
        }
