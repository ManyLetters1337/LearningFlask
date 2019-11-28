from flask import session, jsonify, Blueprint, request
from database.service_registry import services
from flask_login import login_required
from app import page_size

api_projects = Blueprint('api_projects', __name__, url_prefix='/projects')


@api_projects.route('/', methods=['GET'])
@login_required
def projects_page():
    """
    Get method for All Projects Page
    :return:
    """
    page = int(request.args.get('page', default=1))
    projects = services.projects.apply_pagination(services.projects.get_projects_for_user(session['user_id']), page, page_size)

    return jsonify(projects=[project.serialize() for project in projects.items])


@api_projects.route('/<uuid>', methods=['GET'])
@login_required
def project_page(uuid: str):
    """
    Get method for All Projects Page
    :return:
    """
    page = int(request.args.get('page', default=1))
    project = services.projects.get_by_uuid(uuid)
    notes = services.notes.apply_pagination(services.projects.get_notes_for_project(project.id), page, page_size)

    return jsonify(notes=[note.serialize() for note in notes.items], project=project.serialize())

