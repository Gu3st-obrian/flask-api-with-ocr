import sqlite3, click, mysql.connector
from flask import current_app, g
from flask.cli import with_appcontext

def get_dbl():
	if 'dbl' not in g :
		g.dbl = sqlite3.connect(current_app.config['LOCAL_STORAGE'], detect_types = sqlite3.PARSE_DECLTYPES)
		g.dbl.row_factory = sqlite3.Row
	return g.dbl	

def close_dbl():
	dbl = g.pop('dbl', None)
	if dbl is not None:
		dbl.close()

def init_db():
	db = get_dbl()
	import os
	with current_app.open_resource(current_app.config['SCHEMA']) as f :
		db.executescript(f.read().decode('utf8'))

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
	init_db()
	click.echo('Initialization of database.')

def get_instance():
	credentials = get_dbl().execute("SELECT * FROM credentials WHERE label = '0xcl'").fetchone()
	g.db = mysql.connector.connect(
		host = credentials[2], 
		user = credentials[3], 
		passwd = credentials[4], 
		database = credentials[5]
	)
	close_dbl()

def get_db():
	if 'db' not in g :
		get_instance()
	if not g.db.is_connected() :
		get_instance()
	return g.db

def close_db(e = None):
	db = g.pop('db', None)
	if db is not None:
		db.close()
