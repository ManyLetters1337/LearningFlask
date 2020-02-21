"""
Database interaction methods for a Project class
"""
from database.core import db
from database.base_services import BaseDBService
from notes.models import Note
from .models import Project
from flask import session
from sqlalchemy import func
import uuid
from users.models import User


class ProjectDBService(BaseDBService):
    model = Project

    def create(self, user: User, **kwargs) -> Project:
        """
        Create project instance
        @param user: User instance
        @param kwargs:
        @return: Project instance
        """
        project: Project = super().new(title=kwargs['title'], description=kwargs['description'])
        project.set_user(user)
        project.set_uuid(uuid.uuid4().__str__())

        self.commit()

        return project

    def delete_project(self, uuid_: str):
        """
        Delete project instance
        :param uuid_:
        :return:
        """
        project: Project = self.get_by_uuid(uuid_)

        db.session.delete(project)

        if project.user_id.__str__() == session['user_id'].__str__():
            self.commit()

    def change_project(self, uuid_: str, title: str, description: str) -> Project:
        """
        Change project data
        :param uuid_:
        :param title:
        :param description:
        :return:
        """
        project: Project = self.get_by_uuid(uuid_)
        project.title = title
        project.description = description

        if project.user_id.__str__() == session['user_id'].__str__():
            self.commit()

        return project

    def get_notes_for_project(self, id_):
        """
        Get note for current project
        :param id_:
        :return:
        """
        return db.session.query(Note).filter(Note.project_id == id_).order_by(db.desc(Note.created_on))

    def get_projects(self, user: 'User') -> Project:
        """
        Get projects
        :return: List of all project
        """
        return self.filter(user=user)

    def get_projects_for_user(self, user: User) -> Project:
        """
        Get projects for current user
        :param user:
        :return: List of projects for user
        """
        return self.filter(user=user).order_by(db.desc(Project.created_on))

    def get_projects_for_form(self, user: User) -> Project:
        """
        Get projects for form
        :param user: User Instance
        :return: List of projects for form
        """
        return self.filter(user=user).all()

    def get_statistics(self, user: User, **kwargs) -> dict:
        """
        Get statistics for user projects
        :param user: User instance
        :return:
        """
        stat_for_note = db.session.query(Note.project_id, Note.status, Project.title, Project.uuid, func.count()).\
            filter(self.model.user.has(id=user.id)).filter_by(**kwargs).group_by(Note.project_id, Note.status).\
            filter(Project.id == Note.project_id)

        check_list = set()
        statistics = {}

        for values in stat_for_note:

            if values.title in check_list:
                statistics[values.title][values.status] = values[4]
                continue

            statistics[values.title] = {values.status: values[4]}
            statistics[values.title]['uuid'] = values.uuid

            check_list.add(values.title)

        return statistics
