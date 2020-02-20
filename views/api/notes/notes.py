from flask import session, request, jsonify, Blueprint
from database.service_registry import services
from flask_login import login_required
from typing import TYPE_CHECKING
from config import page_size

if TYPE_CHECKING:
    from notes.models import Note

api_notes = Blueprint('api_notes', __name__)


@api_notes.route('/', methods=['GET'])
@login_required
def notes_page():
    """
    Get method for All Notes Page
    :return:
    """
    page = int(request.args.get('page', default=1))
    user = services.users.get_by_id(session['user_id'])
    notes = services.notes.apply_pagination(services.notes.get_notes_for_user(user), page, page_size)

    return jsonify(notes=[note.serialize() for note in notes.items])


@api_notes.route('/<uuid>', methods=['GET'])
@login_required
def note_page(uuid: str):
    """
    Get method for Note Page
    :param uuid:
    :return:
    """
    note_: 'Note' = services.notes.get_by_uuid(uuid)
    return jsonify(note_.serialize())


@api_notes.route('/all', methods=['GET'])
@login_required
def get_all_note():
    """
    Get all Notes
    @return:
    """
    notes = services.notes.get_all()
    return jsonify([note.serialize() for note in notes])
