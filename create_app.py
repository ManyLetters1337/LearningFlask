import os
from flask import Flask
from database.core import db
from flask_login import LoginManager

login_manager = LoginManager()


def create_app(db_url, register_blueprint):
    app = Flask(__name__)
    app.debug = True

    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    db.init_app(app)

    login_manager.init_app(app)

    if register_blueprint:
        register_blueprints(app)

    return app


def register_blueprints(app):
    from views.users.auth import auth
    from views.users.users import users
    from views.notes.notes import notes
    from views.projects.projects import projects
    from views.product.product import product
    from views.angular.angular import angular
    from views.errors.errors import page_not_found

    from views.api.notes.notes import api_notes
    from views.api.projects.projects import api_projects
    from views.api.users.users import api_users

    app.register_blueprint(notes, url_prefix='/notes')
    app.register_blueprint(projects, url_prefix='/projects')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(product, url_prefix='/product')
    app.register_blueprint(angular, url_prefix='/angular')
    app.register_error_handler(404, page_not_found)

    app.register_blueprint(api_notes, url_prefix='/api/notes')
    app.register_blueprint(api_users, url_prefix='/api/users')
    app.register_blueprint(api_projects, url_prefix='/api/projects')


