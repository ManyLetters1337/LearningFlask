from flask import session, jsonify, Blueprint
from database.service_registry import services
from flask_login import login_required


api_users = Blueprint('api_users', __name__, url_prefix='/users')
