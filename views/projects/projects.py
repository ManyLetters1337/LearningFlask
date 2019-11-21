"""
Views for Project Class
"""
from app import app
from flask import url_for, render_template, redirect, session, request
from form.forms import ProjectForm
from database.service_registry import services
from flask_login import login_required
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from projects.models import Project


@app.route('/projects', methods=['GET'])
@login_required
def projects_page():
    if 'user_id' in session:
        return render_template("projects/projects.html",
                               projects=services.projects.get_projects_for_user(session["user_id"]))
    else:
        return render_template("projects/projects.html")


@app.route('/add_project', methods=['POST', 'GET'])
@login_required
def add_project():
    form: ProjectForm = ProjectForm()

    if form.validate_on_submit():
        project_: 'Project' = services.projects.create(form.title.data, form.description.data,
                                                       session['user_id'])
        return redirect(url_for('projects_page'))

    return render_template('projects/add_project.html', form=form)


@app.route('/projects/<uuid>/', methods=['POST', 'GET'])
@login_required
def project(uuid: str):
    form: ProjectForm = ProjectForm()
    project_ = services.projects.get_by_uuid(uuid)
    form.description.data = project_.description
    notes = services.projects.get_notes_for_project(project_.id)

    if form.validate_on_submit():
        if request.form['button'] == 'Delete':
            services.projects.delete_project(uuid)
        elif request.form['button'] == 'Change':
            project_: 'Project' = services.projects.change_project(uuid, form.title.data,
                                                                   request.form['description'])

        return redirect(url_for('projects_page'))

    return render_template('projects/project.html', project=project_, form=form, notes=notes)
