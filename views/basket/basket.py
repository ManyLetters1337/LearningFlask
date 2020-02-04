"""
Views for Basket Class
"""
from flask import url_for, render_template, redirect, session, request, Blueprint
from database.service_registry import services
from flask_login import login_required


basket = Blueprint('basket', __name__, template_folder='templates')


@basket.route('/basket', methods=['GET'])
@login_required
def basket_page():
    """
    Page with basket
    :return: Page with basket
    """

    return render_template("/basket.html")


