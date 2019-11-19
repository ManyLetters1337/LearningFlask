"""
Database interaction methods for a User class
"""
from database.base_services import BaseDBService
from database.core import db
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound
from .models import User


class UserDBService(BaseDBService):
    model = User

    def get_password_hash(self, username: str) -> 'password_hash': # ???
        """
        Get password_hash for user
        :param username:
        :return: Password_hash or
        """
        try:
            return db.session.query(User).filter(User.username == username).first().password_hash
        except NoResultFound as e:
            raise NotFound()

    def get_id_by_name(self, username: str) -> id:
        """
        Get user id by name
        :param username:
        :return: User id or NotFound
        """
        try:
            return db.session.query(User).filter(User.username == username).first().id
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
            return db.session.query(User).filter(User.username == username).first()
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
        user: User = super(UserDBService, self).create(username=username, email=email)
        user.set_password(password)

        db.session.commit()

        return user
