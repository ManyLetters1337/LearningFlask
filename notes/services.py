"""
Database interaction methods for a Note class
"""
from database.core import db
from database.base_services import BaseDBService
from .models import Note
from flask import session
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from users.models import User


class NoteDBService(BaseDBService):
    model = Note

    def get_notes_for_user(self, user: 'User') -> Note:
        """
        Get note for current user
        :param user_id:
        :return  Notes for user
        @param user:
        """
        return db.session.query(self.model).filter(self.model.user.any(id=user.id)).order_by(db.desc(Note.created_on))

    def create(self, user: 'User', **kwargs) -> Note:
        """
        Create Note Instance
        @param user:
        @param kwargs:
        @return:
        """
        note: Note = super(NoteDBService, self).new(title=kwargs['title'],
                                                    description=kwargs['description'],
                                                    status=kwargs['status'])
        note.set_created_by(user)
        note.set_project(kwargs['project'])
        user.note.append(note)
        note.set_uuid(uuid.uuid1().__str__())

        self.commit()

        return note

    def assign_user(self, note: 'Note', user: 'User'):
        """
        Assigne
        @param user_id:
        @param note:
        @param user:
        @return:
        """
        note.user.append(user)

        self.commit()

    def delete_note(self, uuid_: str, user: 'User'):
        """
        Delete Note
        :param uuid_:
        :return:
        @param uuid_:
        @param user:
        """
        note: Note = self.get_by_uuid(uuid_)

        db.session.delete(note)

        if user in note.user:
            self.commit()

    def change_note(self, uuid_: str, user: 'User', **kwargs) -> Note:
        """
        Change Note Instance
        @param user:
        @param uuid_: UUID of note instance
        @param kwargs: Title or another field to changing
        @return:
        """
        note: Note = self.get_by_uuid(uuid_)
        note.title = kwargs['title']
        note.description = kwargs['description']
        note.status = kwargs['status']
        note.set_project(kwargs['project'])

        if user in note.user:
            self.commit()

        return note
