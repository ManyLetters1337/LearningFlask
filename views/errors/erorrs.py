"""
Errors view class
"""
from flask import render_template
from app import app


@app.errorhandler(404)
def not_exist(e):
    message = "This note dos'not exist"

    return render_template("errors/errors.html", title="Not Exist", message=message)


@app.errorhandler(401)
def unauthorized(e):
    message = "You must be logged in to view this note"

    return render_template("errors/errors.html", title="Unauthorized user", message=message)
