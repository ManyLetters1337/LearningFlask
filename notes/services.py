"""
Database interaction methods for a Note class
"""
from database.core import db
from database.base_services import BaseDBService
from typing import TYPE_CHECKING
from .models import Note


# if TYPE_CHECKING:


class NoteDBService(BaseDBService):
    model = Note

    def get_notes(self) -> 'Note':
        """
        Get notes
        :return: List of all notes
        """
        return db.session.query(Note).all()

    def get_notes_for_user(self, user_id: int) -> 'Note':
        """
        Get note for current user
        :param user_id:
        :return: List of notes for user
        """
        return db.session.query(Note).filter(Note.user_id == user_id).order_by(db.desc(Note.created_on)).all()

    # def get_id_by_title_and_description(self, title: str, description: str) -> db.Model:
    #     """
    #     Get note by title and description
    #     :param title:
    #     :param description:
    #     :return:
    #     """
    #     print(db.session.query(Note).filter(Note.title == title and Note.description == description).first().id)
    #     return db.session.query(Note).filter(Note.title == title and Note.description == description).first()

    def create(self, title: str, description: str, user_id: int) -> 'Note':
        """
        Create note instance
        :param title:
        :param description:
        :param user_id:
        :return: Note instance
        """
        note = super(NoteDBService, self).create(title=title, description=description, status=False)
        note.set_user(user_id)

        db.session.commit()  # уточнить

        return note

    # def delete_note(self, title: str, description: str) -> db.Model:
    #     note = self.get_id_by_title_and_description(title, description)
    #     db.session.delete(note)
    #     db.session.commit()
