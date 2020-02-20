from flask import session, jsonify, Blueprint
from database.service_registry import services
from flask_login import login_required
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import User


api_users = Blueprint('api_users', __name__, url_prefix='/users')


@api_users.route('/all_users', methods=['GET'])
@login_required
def get_all_user():
    """
    Get All Users
    @return:
    """

    users = services.users.get_all()

    return jsonify([user.serialize() for user in users])


@api_users.route('/<uuid>', methods=['GET'])
@login_required
def get_user_data_by_uuid(uuid):
    """
    Get Data for Specific User
    @param uuid: User uuid
    @return:
    """
    user: 'User' = services.users.get_by_uuid(uuid)

    return jsonify(user.serialize())


@api_users.route('/id/<user_id>', methods=['GET'])
@login_required
def get_user_data_by_id(user_id):
    """
    Get Data for Specific User
    @param id:
    @param uuid: User uuid
    @return:
    """
    user: 'User' = services.users.get_by_id(user_id)

    return jsonify(user.serialize())


@api_users.route('/projects/<uuid>', methods=['GET'])
@login_required
def get_projects_for_user(uuid):
    """
    Get Projects For Specific User
    @param uuid:
    @return:
    """
    user: 'User' = services.users.get_by_uuid(uuid)

    projects = services.projects.get_projects_for_user(user)

    return jsonify([project.serialize() for project in projects])


@api_users.route('/notes/<uuid>', methods=['GET'])
@login_required
def get_notes_for_user(uuid):
    """
    Get Notes For Specific User
    @param uuid:
    @return:
    """
    user: 'User' = services.users.get_by_uuid(uuid)

    notes = services.notes.get_notes_for_user(user)

    return jsonify([note.serialize() for note in notes])

