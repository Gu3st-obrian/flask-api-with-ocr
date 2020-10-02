import os
from flask import Flask, request
from flask_cors import CORS

def create_app(test_config = None):
	boot = AppBooter(Flask(__name__, instance_relative_config = True))
	boot.kernel(test_config)
	boot.routes()
	app = boot.start()
	cors = CORS(app, resources = {r'/*': {"origins": "*"}})
	return app


class AppBooter(object):
	def __init__(self, app):
		self.app = app

	def start(self):
		return self.app	

	def kernel(self, test_config):
		self.app.config.from_mapping(
			CORS_HEADERS = 'Content-Type',
			SECRET_KEY = 'i4mth3b35tw3bm@5t3rh3r3',
			LOCAL_STORAGE = os.path.join(self.app.instance_path, 'flaskr.sqlite3'),
			SCHEMA = os.path.join(self.app.instance_path, 'schema.sql')
		)
		if test_config is None :
			self.app.config.from_pyfile('config.py', silent = True)
		else :
			self.app.config.from_mapping(test_config)
		try:
			os.makedirs(self.app.instance_path)
		except OSError:
			pass
		from flaskr.models import db
		db.init_app(self.app)

	def routes(self):
		# Page d'accueil.
		from . import Index
		self.app.register_blueprint(Index.bp)
		# Authentification de l'utilisateur de l'API.
		from . import Api
		self.app.register_blueprint(Api.bp)
		# UserController
		from . import User
		self.app.register_blueprint(User.bp)
		# CodeController
		from . import Code
		self.app.register_blueprint(Code.bp)
		#############################
		# Gestion des erreurs http. #
		#############################
		@self.app.errorhandler(404)
		def page_not_found(e):
			return {'statut' : 400, 'msg' : "La ressource demandée est introuvable ou une information est manquante."}, 200

		@self.app.errorhandler(405)
		def page_not_found(e):
			return {'statut' : 400, 'msg' : "La méthode utilisée n'est pas associée à cette ressource."}, 200

		@self.app.errorhandler(500)
		def page_not_found(e):
			return {'statut' : 400, 'msg' : "Aucune ressource disponible pour l'instant."}, 200

		@self.app.errorhandler(502) # Bad Gateway
		def page_not_found(e):
			return {'statut' : 400, 'msg' : "La ressource demandée n'existe pas."}, 200
