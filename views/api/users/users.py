from flask import session, jsonify, Blueprint
from database.service_registry import services
from flask_login import login_required


api_users = Blueprint('api_users', __name__, url_prefix='/users')


@api_users.route('/statistics', methods=['GET'])
@login_required
def statistics_page():
    """
    Get method for Statistics Page
    :return:
    """
    statistics = services.users.get_statistics(session['user_id'])

    return jsonify(statistics)
