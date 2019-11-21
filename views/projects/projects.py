"""
Views for Project Class
"""
from app import app
from flask import url_for, render_template, redirect, session, request
# from form.forms import ProjectForm
from database.service_registry import services
from flask_login import login_required
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notes.models import Project


@app.route('/note', methods=['GET'])
def projects_page():

    if 'user_id' in session:
        return render_template("notes/notes.html", notes=services.notes.get_notes_for_user(session["user_id"]),
                               username=services.users.get_by_id(session['user_id']).username)
    else:
        return render_template("notes/notes.html")


@app.route('/add_note', methods=['POST', 'GET'])
@login_required
def add_project():
    form: ProjectForm = ProjectForm()

    if form.validate_on_submit():
        note_: 'Project' = services.notes.create(form.title.data, form.description.data,
                                              session['user_id'], form.status.data)
        return redirect(url_for('notes_page'))

    return render_template('notes/add_note.html', form=form)


