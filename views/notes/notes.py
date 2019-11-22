"""
Views for Note Class
"""
from app import app
from app import page_size
from flask import url_for, render_template, redirect, session, request, Blueprint
from form.forms import NoteForm
from database.service_registry import services
from flask_login import login_required
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notes.models import Note


@app.route('/', methods=['GET'])
@app.route('/note', methods=['GET'])
@app.route('/note/<int:page>', methods=['GET'])
@login_required
def notes_page(page=1):
    """
    Page with notes
    :return: Page with notes
    """
    if 'user_id' in session:
        return render_template("notes/notes.html", notes=services.notes.apply_pagination(
            services.notes.get_notes_for_user(session["user_id"]), page, page_size))
    else:
        return render_template("notes/notes.html")


@app.route('/add_note', methods=['POST', 'GET'])
@login_required
def add_note():
    """
    Page for Add Note
    :return: Page with Add Note form or Page with Notes
    """
    form: NoteForm = NoteForm()
    projects = services.projects.get_projects_for_form(session['user_id'])
    form.project.choices = [(project.id, project.title) for project in projects]

    if form.validate_on_submit():
        note_: 'Note' = services.notes.create(form.title.data, form.description.data,
                                              session['user_id'], form.status.data, form.project.data)
        return redirect(url_for('notes_page'))

    return render_template('notes/add_note.html', form=form)


@app.route('/note/<uuid>/', methods=['POST', 'GET'])
@login_required
def note(uuid: str):
    """
    Page with Note
    :param uuid:
    :return:
    """
    form: NoteForm = NoteForm()
    note_instance = services.notes.get_by_uuid(uuid)
    projects = services.projects.get_projects_for_form(session['user_id'])

    form.description.data = note_instance.description
    form.status.data = note_instance.status
    form.project.choices = [(project.id, project.title) for project in projects]
    form.project.data = note_instance.project_id

    if form.validate_on_submit():
        if request.form['button'] == 'Delete':
            services.notes.delete_note(uuid)
        elif request.form['button'] == 'Change':
            note_: 'Note' = services.notes.change_note(uuid, form.title.data,
                                                       request.form['description'], request.form['status'],
                                                       request.form['project'])
        return redirect(url_for('notes_page'))

    return render_template('notes/note.html', note=note_instance, form=form)
