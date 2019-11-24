"""
Database interaction methods for a User class
"""
from database.base_services import BaseDBService
from database.core import db
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, case
from werkzeug.exceptions import NotFound
from .models import User
from notes.models import Note
from projects.models import Project
import uuid


class UserDBService(BaseDBService):
    model = User

    def get_password_hash(self, username: str) -> 'password_hash':
        """
        Get password_hash for user
        :param username:
        :return: Password_hash or
        """
        try:
            return self.filter(username=username).first().password_hash
        except NoResultFound as e:
            raise NotFound()

    def get_id_by_name(self, username: str) -> id:
        """
        Get user id by name
        :param username:
        :return: User id or NotFound
        """
        try:
            return self.filter(username=username).first().id
        except NoResultFound as e:
            raise NotFound()

    def get_user_by_name(self, username: str) -> User:
        """
        Get user by username
        :param username:
        :return: User instance
        :raise NotFound: if user instance not found
        """
        try:
            return self.filter(username=username).first()
        except NoResultFound as e:
            raise NotFound()

    def create(self, username: str, email: str, password: str) -> User:
        """
        Create user instance
        :param username:
        :param email:
        :param password:
        :return: User instance
        """
        user: User = super(UserDBService, self).new(username=username, email=email)
        user.set_password(password)
        user.set_uuid(uuid.uuid1().__str__())

        self.commit()

        return user

    def get_statistics(self, id_: int):
        # return db.session.query(User.username, Project.title, func.count(Note.status).label('status')).\
        #     filter(User.id == Project.user_id).filter(Project.id == Note.project_id).\
        #     group_by(User.username, Project.title, Note.status).filter_by(id=id_)

        return db.session.query(Project.title, func.count(case([(Note.status == "Open", 1)])).label("open"),
                                func.count(case([(Note.status == "In Progress", 1)])).label("in_progress"),
                                func.count(case([(Note.status == "Resolved", 1)])).label("resolved"),
                                func.count(case([(Note.status == "Closed", 1)])).label("closed")).\
            group_by(Project.title).filter(Project.id == Note.project_id).filter_by(user_id=id_)
