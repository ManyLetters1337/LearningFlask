"""
Views for Note Class
"""
from app import app
from flask import url_for, render_template, redirect, session, request
from form.forms import AddNoteForm
from database.service_registry import services
from flask_request_params import bind_request_params


@app.route('/note', methods=['POST', 'GET'])
def notes_page():
    """
    Page with notes
    :return: Page with notes
    """
    if 'user_id' in session:
        return render_template("notes/notes.html", notes=services.notes.get_notes_for_user(session["user_id"]))
    else:
        return render_template("notes/notes.html")


@app.route('/add_note', methods=['POST', 'GET'])
def add_note():
    """
    Page for Add Note
    :return: Page with Add Note form or Page with Notes
    """
    form = AddNoteForm()

    if form.validate_on_submit():
        services.notes.create(form.title.data, form.description.data, session['user_id'])
        return redirect(url_for('notes_page'))

    return render_template('notes/add_note.html', form=form)


@app.route('/note/<uuid>/', methods=['POST', 'GET'])
def note(uuid: str):
    print(uuid)
    form = AddNoteForm()
    note_instance = services.notes.get_by_uuid(uuid)
    form.description.data = note_instance.description
    if form.validate_on_submit():
        pass

    return render_template('notes/note.html', note=note_instance, form=form)
