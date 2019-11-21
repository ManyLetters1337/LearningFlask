"""
Errors view class
"""
from flask import render_template, request, redirect
from app import app


@app.errorhandler(404)
def not_exist(e):
    """
    If Page don'not exist
    :param e:
    :return:
    """
    message = "This page dos'not exist"

    return render_template("errors/errors.html", title="Not Exist", message=message)


# @app.errorhandler(401)
# def unauthorized(e):
#     """
#     If user don't unauthorized
#     :param e:
#     :return:
#     """
#     message = "You must be logged in to view this note"
#
#     return render_template("errors/errors.html", title="Unauthorized user", message=message)
