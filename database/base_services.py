"""
Сlass with the basic methods of interacting with the database
"""
from sqlalchemy.orm import Query
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound
from projects.models import Project
from .core import db
from typing import Union
import uuid


class BaseDBService:
    model = None

    def get_by_id(self, id_: int) -> db.Model:
        """
        Get instance by id
        :param id_:
        :return: instance or NotFound
        :raise NotFound: if instance not found
        """
        try:
            return db.session.query(self.model).filter_by(id=id_).one()
        except NoResultFound as e:
            raise NotFound()

    def get_by_id_or_none(self, id_: int) -> Union[db.Model, None]:
        """
        Get instance by id
        :param id_:
        :return: instance or none
        """
        return db.session.query(self.model).filter_by(id=id_).first()

    def get_by_uuid(self, uuid_: str) -> db.Model:
        """
        Get instance by uuid
        :param uuid_:
        :return: instance or NotFound
        :raise  NotFound: if instance not found
        """
        try:
            return db.session.query(self.model).filter_by(uuid=uuid_).one()
        except NoResultFound as e:
            raise NotFound()

    def get_by_uuid_or_none(self, uuid_: str) -> Union[db.Model, None]:
        """
        Get instance by uuid
        :param uuid_:
        :return: instance or none
        """
        return db.session.query(self.model).filter_by(uuid=uuid_).first()

    def get_all(self):
        """
        Get all instance
        @return:
        """
        return db.session.query(self.model).all()

    def get_uuid_by_id(self, id_: int) -> uuid:
        """
        Get uuid by id
        :param id_:
        :return: uuid for instance
        """
        return db.session.query(self.model.uuid).filter_by(id=id_).first().uuid

    def filter(self, **kwargs):
        """
        Filter
        :param kwargs:
        :return:
        """
        return db.session.query(self.model).filter_by(**kwargs)

    def apply_pagination(self, query: Query, start_page: int, page_size: int) -> Query:
        """
        Apply pagination for page
        :param query:
        :param start_page:
        :param page_size:
        :return:
        """
        start_page = self.validate_page_size(start_page)
        return query.paginate(start_page, page_size)

    def new(self, **kwargs) -> db.Model:
        """
        Create instance
        :param kwargs: Params for Instance
        :return: Instance
        """
        instance = self.model(**kwargs)

        db.session.add(instance)

        return instance

    def validate_page_size(self, start_page):
        """
        Validate start page
        @param start_page:
        @return: Validate start page
        """
        if start_page < 1:
            start_page = 1
        return start_page

    def commit(self):
        """
        Make Commit
        :return:
        """
        db.session.commit()

    def get_title_by_id(self, id_: int) -> 'title':
        """
        Get title by id
        :param id_: Instance id
        :return: Title for this instance
        """
        return db.session.query(Project).filter_by(id=id_).first().title
