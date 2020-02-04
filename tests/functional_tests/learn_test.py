import unittest

from config import Statuses
import pytest
from werkzeug.security import generate_password_hash, check_password_hash
from database.service_registry import services
from tests.factories.note import NoteFactory
from tests.factories.project import ProjectFactory
from tests.factories.user import UserFactory

TEST_DB = 'test.db'


@pytest.mark.usefixtures('init_notes_app')
class BasicTests(unittest.TestCase):

    def test_statistics_count(self):
        project1 = ProjectFactory(title='project1')
        project2 = ProjectFactory(title='project2')
        project3 = ProjectFactory(title='project3')
        user = UserFactory(username="UserName1", password_hash=generate_password_hash("12345"), email="some1@mail.ru")
        NoteFactory(title="note1", project_id=project1.id, user=user)
        NoteFactory(title="note1", project_id=project2.id, user=user)
        NoteFactory(title="note1", project_id=project3.id, user=user)

        result = services.projects.get_statistics(user=user)
        self.assertEqual(len(result), 3)

    def test_statistics_with_status(self):
        project = ProjectFactory(title='project2')
        user = UserFactory(username="UserName2", password_hash=generate_password_hash("12345"), email="some2@mail.ru")

        NoteFactory(title="noteCLOSED1", project_id=project.id, user=user, status=Statuses.CLOSED.value)
        NoteFactory(title="noteCLOSED2", project_id=project.id, user=user, status=Statuses.CLOSED.value)
        NoteFactory(title="noteCLOSED3", project_id=project.id, user=user, status=Statuses.CLOSED.value)

        NoteFactory(title="noteRESOLVED1", project_id=project.id, user=user, status=Statuses.RESOLVED.value)

        NoteFactory(title="noteIN_PROGRESS1", project_id=project.id, user=user, status=Statuses.IN_PROGRESS.value)

        NoteFactory(title="noteOPEN1", project_id=project.id, user=user, status=Statuses.OPEN.value)
        NoteFactory(title="noteOPEN2", project_id=project.id, user=user, status=Statuses.OPEN.value)

        result = services.projects.get_statistics(user=user)

        self.assertEqual(result[project.title][Statuses.RESOLVED.value], 1)
        self.assertEqual(result[project.title][Statuses.IN_PROGRESS.value], 1)
        self.assertEqual(result[project.title][Statuses.CLOSED.value], 3)
        self.assertEqual(result[project.title][Statuses.OPEN.value], 2)

    def test_user_create(self):
        test_cases = [
            {
                'username': 'UserNameTest1',
                'mail': 'UserMail1@mail.ru',
                'password': '12345678*Aa'
            },
            {
                'username': 'UserNameTest2',
                'mail': 'UserMail2@mail.ru',
                'password': '12345678*Aa'
            },
            {
                'username': '123',
                'mail': '123@mail.ru',
                'password': '12345678*Aa'
            }
        ]
        for test_case in test_cases:
            user = services.users.create(test_case['username'], test_case['mail'], test_case['password'])

            self.assertEqual(user.username, test_case['username'])

            self.assertTrue(check_password_hash(user.password_hash, test_case['password']))

            self.assertEqual(user.email, test_case['mail'])

    def test_user_creation_bad_data(self):
        with self.assertRaises(Exception):
            services.users.create("UserName4", "some4@mail.ru", None)
        with self.assertRaises(Exception):
            services.users.create("UserName4", None, None)
        with self.assertRaises(Exception):
            services.users.create("UserName4", None, "12345678*Aa")
        with self.assertRaises(Exception):
            services.users.create(None, "some4@mail.ru", "12345678*Aa")

    def test_pagination_bad_start(self):
        page_size = 3
        user = UserFactory(username="UserName5", password_hash=generate_password_hash("12345"), email="some5@mail.ru")

        ProjectFactory(title='project1', user=user)
        ProjectFactory(title='project2', user=user)
        ProjectFactory(title='project1', user=user)
        ProjectFactory(title='project1', user=user)

        result = services.projects.apply_pagination(services.projects.get_projects_for_user(user), 0, page_size)

        self.assertEqual(len(result.items), 3)
        self.assertTrue(result.has_next)
        self.assertFalse(result.has_prev)

    def test_pagination_valid_start(self):
        page_size = 3
        user = UserFactory(username="UserName6", password_hash=generate_password_hash("12345"), email="some6@mail.ru")

        ProjectFactory(title='project1', user=user)
        ProjectFactory(title='project2', user=user)
        ProjectFactory(title='project1', user=user)
        ProjectFactory(title='project1', user=user)

        result = services.projects.apply_pagination(services.projects.get_projects_for_user(user), 2, page_size)

        self.assertEqual(len(result.items), 1)
        self.assertFalse(result.has_next)
        self.assertTrue(result.has_prev)

    def test_start_page_validation_bad_start_page(self):
        start_page = 0
        start_page = services.projects.validate_page_size(start_page)

        self.assertEqual(start_page, 1)

    def test_start_page_validation_valid_start_page(self):
        start_page = 5
        start_page = services.projects.validate_page_size(start_page)

        self.assertEqual(start_page, 5)

    def test_create_project_for_user(self):
        user = UserFactory(username="ProjectTest", email="ProjectMail@mail.ru", password_hash=generate_password_hash("123"))
        test_cases = [
            {
                'title': 'Project Title 1',
                'description': 'Project Description 1'
            },
            {
                'title': 'Project Title 2',
                'description': 'Project Description 2'
            },
            {
                'title': '123',
                'description': '123'
            },
            {
                'title': 'Project',
                'description': ''
            },
        ]

        for test_case in test_cases:
            project = services.projects.create(user, title=test_case['title'], description=test_case['description'])

            self.assertEqual(project.title, test_case['title'])
            self.assertEqual(project.description, test_case['description'])
            self.assertEqual(project.user, user)

    def test_create_project_bad_data(self):
        with self.assertRaises(Exception):
            services.projects.create(user=None, title="Test Project", description="Without User")

        with self.assertRaises(Exception):
            services.projects.create(title="Test Project", description=None)

        with self.assertRaises(Exception):
            services.projects.create(user=None, title=None, description=None)

    def test_create_note_for_user(self):
        user = UserFactory(username="NotesTest", email="NotesMail@mail.ru", password_hash=generate_password_hash("123"))
        project = services.projects.create(user, title="Test Project Title", description="Test Project Descr")
        test_cases = [
            {
                'title': 'Note Title 1',
                'description': 'Note Description 1',
                'status': Statuses.RESOLVED.value
            },
            {
                'title': 'Note Title 2',
                'description': 'Note Description 2',
                'status': Statuses.OPEN.value
            },
            {
                'title': '123',
                'description': '123',
                'status': Statuses.CLOSED.value
            },
            {
                'title': 'Note',
                'description': '',
                'status': Statuses.IN_PROGRESS.value
            },
        ]

        for test_case in test_cases:
            notes = services.notes.create(user, title=test_case['title'], description=test_case['description'],
                                          status=test_case['status'], project=project)

            self.assertEqual(notes.title, test_case['title'])
            self.assertEqual(notes.description, test_case['description'])
            self.assertEqual(notes.project, project)
            self.assertEqual(notes.user, user)

    def test_create_note_bad_data(self):
        with self.assertRaises(Exception):
            services.notes.create(title="Test Note", description="Without User", status=None)

        with self.assertRaises(Exception):
            services.notes.create(title="Test Note", description=None, status=None)

        with self.assertRaises(Exception):
            services.notes.create(title=None, description=None, status=None)



