from flask import url_for, render_template, redirect, session, request, Blueprint

angular = Blueprint('angular', __name__, template_folder='templates')


@angular.route('/', methods=['GET'])
def angular_main_page():
    return render_template("/angular_main_page.html")



