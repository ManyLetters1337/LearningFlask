from app import app
from views.notes.notes import notes
from views.projects.projects import projects
from views.users.auth import auth
from views.users.users import users
from views.errors.errors import page_not_found
from views.api.notes.notes import api_notes
from views.api.projects.projects import api_projects
from views.api.users.users import api_users


app.register_blueprint(notes, url_prefix='/notes')
app.register_blueprint(projects, url_prefix='/projects')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(users, url_prefix='/users')
app.register_error_handler(404, page_not_found)

app.register_blueprint(api_notes, url_prefix='/api/notes')
app.register_blueprint(api_users, url_prefix='/api/users')
app.register_blueprint(api_projects, url_prefix='/api/projects')







