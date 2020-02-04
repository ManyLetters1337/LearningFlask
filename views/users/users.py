"""
Views for User Class
"""
from flask import render_template, Blueprint
from flask_login import login_required

users = Blueprint('users', __name__, template_folder='views/users/')


@users.route('/basket', methods=['GET'])
@login_required
def basket_page():
    """
    Page with user basket
    :return: Page with user basket
    """

    return render_template("/basket.html")


