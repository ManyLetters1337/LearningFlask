"""
Configs
"""
import os

from flask import Flask
from flask_restful import Api


# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
app = Flask(__name__)
app.debug = True
api = Api(app)
page_size = 10
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://manyletters:12345678*Aa@localhost/base'

import views

