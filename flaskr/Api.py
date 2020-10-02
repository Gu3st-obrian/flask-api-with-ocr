import functools
from flask import Blueprint, request, g, current_app
import flaskr.models.medoo as medoo

bp = Blueprint('api', __name__, url_prefix = '/api')

@bp.route('/init', methods = ['POST'])
def init():
	try :
		req_data = request.get_json(force=True)
		username = encodePassword(req_data['username'])
		password = encodePassword(req_data['password'])
	except Exception :
		return {'statut': 400, 'msg': "Les données d'authentification sont manquantes."}

	if username is None :
		return {'statut': 400, 'msg': "Authentification incorrecte."}
	elif password is None :
		return {'statut': 400, 'msg': "Authentification incorrecte."}
	else :
		SQL = "SELECT clientname, uniqkey FROM apikeys WHERE isactif = 1 AND username = '{}' AND motdepasse = '{}'".format(username, password)
		result = medoo.query(SQL, True)
		if result is None :
			return {'statut': 400, 'msg': "Authentification incorrecte."}
		return {'statut': 200, 'msg': result[0], 'apikey': result[1]}

def api_auth_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		result = medoo.query("SELECT expiration FROM apikeys WHERE uniqkey = '{}'".format(kwargs['apikey']), True)
		if result is None :
			return {'statut': 400, 'msg': "L'authentification de l'API a échouée."}
		else :
			from datetime import datetime
			now = datetime.now()
			if now >= result[0] :
				from datetime import timedelta
				now = datetime.strptime('{:%Y-%m-%d %H:%M:%S}'.format(now), '%Y-%m-%d %H:%M:%S') + timedelta(hours=2)
				medoo.query("UPDATE apikeys SET expiration = '{}' WHERE uniqkey = '{}'".format(now, kwargs['apikey']))
				if medoo.error() != "0000" :
					return {'statut': 403, 'msg': "La session de votre API a expiré."}
		return view(**kwargs)
	return wrapped_view

def encodePassword(passwd):
	import hashlib
	encoder = 'utf8'
	dk = hashlib.pbkdf2_hmac('sha256', bytes(passwd, encoder), bytes(current_app.config['SECRET_KEY'], encoder), 3003)
	return dk.hex()
