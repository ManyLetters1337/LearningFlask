from flask import Flask, flash, url_for, session, request, render_template, redirect


app = Flask(__name__)
app.debug = True

from flaskext.mysql import MySQL



mysql = MySQL()
mysql.init_app(app)
cursor = mysql.get_db().cursor()



if __name__ == '__main__':
	app.run();