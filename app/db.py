import mysql.connector
from flask import g, current_app

def init_db(app):
	app.config['db_pool'] = mysql.connector.connect(
	host = app.config['MYSQL_HOST'],
	user = app.config['MYSQL_USER'],
	password = app.config['MYSQL_PASSWORD'],
	database = app.config['MYSQL_DATABASE'],
	port = app.config['MYSQL_PORT']	
	)

def get_db():
	if 'db' not in g:
		g.db = current_app.config['db_pool']
	return g.db

def close_db(exception=None):
	db = g.pop('db',None)
	if db is not None:
		db.close()
