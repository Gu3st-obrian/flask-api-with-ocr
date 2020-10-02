from .db import get_db
from re import search
from flask import g

def query(statement, oneresult = False):
	g.sqlError = "0000"
	db = get_db()
	curs = db.cursor()
	results = None
	
	state = search(r'^SELECT .+$', statement)
	try:
		curs.execute(statement)
		if state is None :
			db.commit()
		else :
			results = curs.fetchone() if oneresult else curs.fetchall()
	except Exception as e:
		if state is None :
			db.rollback()
		g.sqlError = e
	return results

def error():
	if 'sqlError' in g :
		return g.sqlError
	else :
		return '0000'
