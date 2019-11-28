"""
Views for User Class
"""
from app import app
from flask import url_for, render_template, redirect, session, request, Blueprint
from database.service_registry import services
from flask_login import login_required

users = Blueprint('users', __name__, template_folder='views/users/')


@users.route('/statistics', methods=['GET'])
@login_required
def statistics_page():
    """
    Page with statisctics for user projects
    :param page:
    :return:
    """
    return render_template("statistics/statistics.html", stat=services.users.get_statistics(session['user_id']))
