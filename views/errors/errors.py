"""
Errors view class
"""
from app import app
from flask import render_template, request, redirect, Blueprint

errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def page_not_found(e):
    """
    If Page don'not exist
    :param e:
    :return:
    """
    message = "This page dos'not exist"

    return render_template("errors.html", title="Not Exist", message=message)
