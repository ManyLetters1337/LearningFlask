"""
Initialize classes
"""
from users.services import UserDBService
from notes.services import NoteDBService
from projects.services import ProjectDBService


class ServiceRegistry:

    def __init__(self):
        self.users = UserDBService()
        self.notes = NoteDBService()
        self.projects = ProjectDBService()


services = ServiceRegistry()
