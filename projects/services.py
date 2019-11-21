"""
Database interaction methods for a Project class
"""
from database.core import db
from database.base_services import BaseDBService
from notes.models import Note
from .models import Project
from flask import session
import uuid


class ProjectDBService(BaseDBService):
    model = Project

    def create(self, title: str, description: str, user_id: int) -> Project:
        """
        Create project instance
        :param title:
        :param description:
        :param user_id:
        :return:
        """
        project: Project = super(ProjectDBService, self).new(title=title, description=description)
        project.set_user(user_id)
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
        return db.session.query(Note).filter(Note.project_id == id_).all()

    def get_projects(self) -> Project:
        """
        Get projects
        :return: List of all project
        """
        return db.session.query(Project).all()

    def get_projects_for_user(self, user_id: int) -> Project:
        """
        Get projects for current user
        :param user_id:
        :return: List of projects for user
        """
        return db.session.query(Project).filter(Project.user_id == user_id).order_by(db.desc(Project.created_on)).all()

    def get_projects_for_form(self, user_id: int) -> Project:
        """
        Get projects for form
        :param user_id:
        :return: List of projects for form
        """
        return db.session.query(Project).filter(Project.user_id == user_id).all()
