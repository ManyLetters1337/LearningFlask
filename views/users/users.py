"""
Views for User Class
"""
from app import app
from flask import url_for, render_template, redirect, session, request, Blueprint
from database.service_registry import services
from flask_login import login_required

users = Blueprint('users', __name__, template_folder='views/users/')



