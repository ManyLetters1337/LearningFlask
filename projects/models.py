"""
Project Class
"""
from database.core import db
from datetime import datetime


class Project(db.Model):
    """
    Model of Project
    """
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.now)

    def set_uuid(self, uuid_):
        """
        Set note uuid
        :param uuid_:
        """
        self.uuid = uuid_

    def set_user(self, id_):
        """
        Set user_id in note
        :param id_:
        """
        self.user_id = id_
