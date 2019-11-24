"""
Views for Project Class
"""
from app import app
from app import page_size
from flask import url_for, render_template, redirect, session, request
from database.service_registry import services
from flask_login import login_required


@app.route('/statistics', methods=['GET'])
@login_required
def statistics_page(page=1):
    return render_template("statistics/statistics.html", stat=services.users.get_statistics(session['user_id']))
