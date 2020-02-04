"""
Configs
"""
from create_app import create_app

db_url = 'mysql+pymysql://manyletters:12345678*Aa@localhost/base'
app = create_app(db_url, True)
