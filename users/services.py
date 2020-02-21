"""
Database interaction methods for a User class
"""
from config import secret_key
from database.base_services import BaseDBService
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from werkzeug.exceptions import NotFound
from .models import User
from notes.models import Note
from database.core import db
import jwt
import uuid


class UserDBService(BaseDBService):
    model = User

    def get_password_hash(self, username: str) -> 'password_hash':
        """
        Get password_hash for user
        :param username:
        :return: Password_hash
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

    def get_user_by_email(self, email: str) -> User:
        """
        Get User by Email
        @param email:
        @return:
        """
        try:
            return self.filter(email=email).first()
        except NoResultFound as e:
            raise NotFound()

    def verify_reset_password_token(self, token):
        """
        Verify reset password token and return user Instance
        @param token: Reset Password Token
        @return: User Instance
        """
        id_ = jwt.decode(token, secret_key, algorithms=['HS256'])['reset_password']

        return self.get_by_id_or_none(id_)

    def reset_password(self, user: 'User', password: str):
        """
        Change User Password
        @param user:
        @param password:
        @return:
        """
        user.set_password(password)

        self.commit()

        return user

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

    def get_notes_statistics(self) -> dict:
        """
        Get statistics for user projects
        :param user: User instance
        :return:
        """
        query = db.session.query(User.username, User.id, Note.status, func.count()). \
            group_by(Note.user_id, Note.status). \
            filter(Note.user_id == User.id)

        users_statistic = {}

        check_list = set()
        for values in query:

            if values.username in check_list:
                users_statistic[values.username][values[2]] = values[3]
                continue

            users_statistic[values.username] = {values[2]: values[3]}
            check_list.add(values.username)

        return users_statistic
