"""
Views for Project Class
"""
from app import page_size
from flask import url_for, render_template, redirect, session, request, Blueprint
from form.forms import create_project_form
from database.service_registry import services
from flask_login import login_required
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from projects.models import Project
    from form.forms import ProjectForm

projects = Blueprint('projects', __name__, template_folder="templates")


@projects.route('/', methods=['GET'])
@login_required
def projects_page():
    """
    Page with all projects for current user
    :return:
    """
    page = int(request.args.get('page', default=1))
    if 'user_id' in session:
        project_for_user = services.projects.get_projects_for_user(session["user_id"])
        return render_template("projects.html",
                               projects=services.projects.apply_pagination(project_for_user, page, page_size))
    else:
        return render_template("projects.html")


@projects.route('/add_project', methods=['GET'])
@login_required
def add_project():
    """
    Get Method for Add Project
    :return:
    """
    form: 'ProjectForm' = create_project_form()

    return render_template('add_project.html', form=form)


@projects.route('/add_project', methods=['POST'])
@login_required
def add_project_post():
    """
    Post method for Add Project
    :return:
    """
    form: 'ProjectForm' = create_project_form()

    project_: 'Project' = services.projects.create(form.title.data, form.description.data, session['user_id'])

    return redirect(url_for('projects.projects_page'))


@projects.route('/<uuid>', methods=['GET'])
@login_required
def project(uuid: str):
    """
    Get method for Project Page
    :param uuid:
    :return:
    """
    page = int(request.args.get('page', default=1))
    project_ = services.projects.get_by_uuid(uuid)

    form: 'ProjectForm' = create_project_form(description=project_.description)

    notes_for_user = services.projects.get_notes_for_project(project_.id)
    notes = services.notes.apply_pagination(notes_for_user, page, page_size)

    return render_template('project.html', project=project_, form=form, notes=notes)


@projects.route('/<uuid>', methods=['POST'])
@login_required
def project_post(uuid: str):
    """
    Post method for Project Page
    :param uuid:
    :return:
    """
    page = int(request.args.get('page', default=1))
    project_ = services.projects.get_by_uuid(uuid)
    form: 'ProjectForm' = create_project_form(description=project_.description)
    notes_for_user = services.projects.get_notes_for_project(project_.id)
    notes = services.notes.apply_pagination(notes_for_user, page, page_size)

    if form.validate():
        if request.form['button'] == 'Delete':
            services.projects.delete_project(uuid)
        elif request.form['button'] == 'Change':
            project_: Project = services.projects.change_project(uuid, form.title.data, request.form['description'])

        return redirect(url_for('projects.projects_page'))

    return render_template('project.html', project=project_, form=form, notes=notes)


@projects.route('/statistics', methods=['GET'])
@login_required
def statistics_page():
    """
    Page with statisctics for user projects
    :return:
    """
    return render_template("statistics/statistics.html", stat=services.users.get_statistics(session['user_id']))


@projects.route('/statistics/<uuid>', methods=['GET'])
@login_required
def statistics_for_project_page(uuid: str):
    """
    Page with statisctics for user projects
    :param uuid:
    :return:
    """
    project_id = services.projects.get_by_uuid(uuid).id
    return render_template("statistics/current_project.html", stat=services.users.get_statistics(session['user_id'],
                                                                                                 project_id=project_id))

