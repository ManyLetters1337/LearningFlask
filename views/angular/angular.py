from flask import url_for, render_template, redirect, session, request, Blueprint
from flask_login import login_required

angular = Blueprint('angular', __name__, template_folder='templates')


@angular.route('/', methods=['GET'])
@login_required
def angular_main_page():
    return render_template("/angular_main_page.html")


@angular.route('/templates/phonesList.html', methods=['GET'])
@login_required
def angular_phone_list():
    return render_template("/phonesList.html")


@angular.route('/templates/carsList.html', methods=['GET'])
@login_required
def angular_cars_list():
    return render_template("/carsList.html")


@angular.route('/templates/statistics.html', methods=['GET'])
@login_required
def angular_statistics():
    return render_template("/statistics.html")


@angular.route('/templates/validationErrors.html', methods=['GET'])
@login_required
def validation():
    return render_template("/validationErrors.html")

