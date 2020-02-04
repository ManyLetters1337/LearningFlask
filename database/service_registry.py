
"""
Initialize classes
"""
from users.services import UserDBService
from notes.services import NoteDBService
from projects.services import ProjectDBService
from product.services import ProductDBService


class ServiceRegistry:

    def __init__(self):
        self.users = UserDBService()
        self.notes = NoteDBService()
        self.projects = ProjectDBService()
        self.products = ProductDBService()


services = ServiceRegistry()
