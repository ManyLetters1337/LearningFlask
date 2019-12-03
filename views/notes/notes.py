"""
Views for Note Class
"""
from app import page_size
from flask import url_for, render_template, redirect, session, request, Blueprint
from form.forms import create_note_form
from database.service_registry import services
from flask_login import login_required

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from notes.models import Note
    from form.forms import NoteForm

notes = Blueprint('notes', __name__, template_folder='templates')


@notes.route('/', methods=['GET'])
@login_required
def notes_page():
    """
    Page with notes
    :return: Page with notes
    """
    page = int(request.args.get('page', default=1))
    notes_for_user = services.notes.get_notes_for_user(session["user_id"])

    return render_template(
        "/notes.html",
        notes=services.notes.apply_pagination(notes_for_user, page, page_size)
    )


@notes.route('/add_note', methods=['GET'])
@login_required
def add_note():
    """
    Get method for Add Note
    :return: Page with Add Note form or Page with Notes
    Page for Add Note
    """
    form: 'NoteForm' = create_note_form()

    return render_template('add_note.html', form=form)


@notes.route('/add_note', methods=['POST'])
@login_required
def add_note_post():
    """
    Post method for Add Note
    :return:
    """
    form: 'NoteForm' = create_note_form()
    if form.validate():
        note_: 'Note' = services.notes.create(
            session['user_id'],
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            project_id=form.project.data
        )
        return redirect(url_for('notes.notes_page'))

    return render_template('add_note.html', form=form)


@notes.route('/<uuid>', methods=['GET'])
@login_required
def note(uuid: str):
    """
    Page with Note
    :param uuid:
    :return:
    """
    note_instance: 'Note' = services.notes.get_by_uuid(uuid)
    form = create_note_form(
        description=note_instance.description,
        status=note_instance.status,
        project=note_instance.project_id
    )

    return render_template('note.html', note=note_instance, form=form)


@notes.route('/<uuid>', methods=['POST'])
@login_required
def note_post(uuid: str):
    """
    Post method for Note Page
    :param uuid:
    :return:
    """
    form: 'NoteForm' = create_note_form()
    note_instance: 'Note' = services.notes.get_by_uuid(uuid)

    if form.validate():
        if request.form['button'] == 'Delete':
            services.notes.delete_note(uuid)
        elif request.form['button'] == 'Change':
            note_: 'Note' = services.notes.change_note(uuid, title=form.title.data, description=request.form['description'],
                                                       status=request.form['status'], project=request.form['project'])

        return redirect(url_for('notes.notes_page'))

    return render_template('note.html', note=note_instance, form=form)
