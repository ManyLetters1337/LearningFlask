"""
Views for Note Class
"""
from config import page_size
from flask import url_for, render_template, redirect, session, request, Blueprint
from form.forms import create_note_form
from database.service_registry import services
from flask_login import login_required
from celery_tasks import send_assign_mail

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
    user = services.users.get_by_id(session['user_id'])
    notes_for_user = services.notes.get_notes_for_user(user)

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
    form: 'NoteForm' = create_note_form(session['user_id'])

    return render_template('add_note.html', form=form)


@notes.route('/add_note', methods=['POST'])
@login_required
def add_note_post():
    """
    Post method for Add Note
    :return:
    """
    user = services.users.get_by_id(session['user_id'])
    form: 'NoteForm' = create_note_form(user.id)

    if form.validate():
        project = services.projects.get_by_id(form.project.data)
        note_: 'Note' = services.notes.create(
            user,
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            project=project
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
    user = services.users.get_by_id(session['user_id'])

    form = create_note_form(
        note_instance.user_id,
        description=note_instance.description,
        status=note_instance.status,
        project=note_instance.project_id
    )

    return render_template('note.html', note=note_instance, form=form, check_assign=(note_instance.user_id == user.id))


@notes.route('/<uuid>', methods=['POST'])
@login_required
def note_post(uuid: str):
    """
    Post method for Note Page
    :param uuid:
    :return:
    """
    note_instance: 'Note' = services.notes.get_by_uuid(uuid)
    form: 'NoteForm' = create_note_form(note_instance.user_id, project=note_instance.project_id)
    user: 'User' = services.users.get_by_id(session['user_id'])
    form.user.data = note_instance.user_id

    if form.validate():
        if request.form['button'] == 'Delete':
            services.notes.delete_note(uuid, user)

        elif request.form['button'] == 'Assign':
            assign_user(form, note_instance)

        elif request.form['button'] == 'Change':
            project = services.projects.get_by_id(request.form['project'])
            note_: 'Note' = services.notes.change_note(uuid, user, title=form.title.data,
                                                       description=request.form['description'],
                                                       status=request.form['status'], project=project)

        return redirect(url_for('notes.notes_page'))

    return render_template('note.html', note=note_instance, form=form, check_assign=(note_instance.user_id == user.id))


def assign_user(form, note_):
    """
    Assign user and send email for user
    @param note_: Note
    @param form: Form Data
    @return:
    """
    assigned_user = services.users.get_by_id(request.form['user'])
    services.notes.assign_user(note_, assigned_user)

    send_assign_mail.apply_async(args=[assigned_user.username, assigned_user.email,
                                       url_for('notes.note', uuid=note_.uuid, _external=True)])
