"""
Initialize classes
"""
from users.services import UserDBService
from notes.services import NoteDBService


class ServiceRegistry:

    def __init__(self):
        self.users = UserDBService()
        self.notes = NoteDBService()


services = ServiceRegistry()
