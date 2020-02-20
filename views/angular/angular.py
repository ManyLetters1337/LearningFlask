from flask import url_for, render_template, redirect, session, request, Blueprint
from flask_login import login_required

angular = Blueprint('angular', __name__, template_folder='templates', static_folder='../../static')


@angular.route('/', methods=['GET'])
@login_required
def angular_main_page():
    """
    View For Page with Angular
    @return:
    """
    print(session)
    return render_template("/angular_main_page.html")
