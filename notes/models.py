"""
Note Class
"""
from database.core import db
from datetime import datetime
import uuid
from users.models import association_table


class Note(db.Model):
    """
    Model of Note
    """
    __tablename__ = 'notes'
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String(50), default=uuid.uuid4().__str__(), unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id'), nullable=True, default="None Project")
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    user = db.relationship('User', secondary=association_table, back_populates='note')

    def set_uuid(self, uuid_: uuid):
        """
        Set note uuid
        :param uuid_:
        """
        self.uuid = uuid_

    def set_project(self, project: 'Project'):
        """
        Set Project for Note instance
        @param project: Project Instance
        """
        self.project = project

    def set_user(self, user: 'User'):
        """
        Set User for Note instance
        @param user: User Instance
        """
        self.user.append(user)

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
