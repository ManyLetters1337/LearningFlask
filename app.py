"""
Configs
"""
import os
import logging
from flask import Flask

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
app = Flask(__name__)
app.debug = True
page_size = 2
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://manyletters:12345678*Aa@localhost/base'

from views.notes import notes
from views.users import auth
from views.errors import erorrs
from views.projects import projects