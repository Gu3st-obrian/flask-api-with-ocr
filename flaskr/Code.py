from flask import Blueprint, request
from flaskr.Api import api_auth_required
import flaskr.models.medoo as medoo
import os

rootapp = os.path.dirname(__file__)

bp = Blueprint('code', __name__, url_prefix = '/code')

@bp.route('/quittance/<apikey>', methods = ['POST'])
@api_auth_required
def quittance(apikey):
	try :
		req_data = request.get_json(force=True)
		username = req_data['username']
		commande = int(req_data['commande'])
		montant = float(req_data['montant'])
	except Exception as e :
		return {'statut': 400, 'msg': "Les données requises ne sont pas complètes."}
	if commande > 98500 :
		SQL = "SELECT ordre FROM quittances INNER JOIN psbeepaiements ON uk_paiement = refcmd WHERE userlogin ='{}' AND uk_paiement = {} AND quittances.montant = {}".format(username, commande, montant)
		result = medoo.query(SQL, True)
		if result is None :
			return {'statut': 200, 'msg': "La quittance de la commande {} n'est pas disponible.".format(commande)}
		import base64
		content = ""
		try :
			with open(os.path.join(rootapp, "uittanx", "psbee", '{}.jpg'.format(commande if result[0] == 1 else '{}_{}'.format(commande, result[0]))), 'rb') as img :
				content = base64.b64encode(img.read())
		except Exception as e :
			return {'statut': 400, 'msg': "La référence {} n'est plus disponible.".format(commande)}
		return {'statut': 200, 'msg': "La quittance {} a été trouvée.".format(commande), 'img': "{}".format(content.decode('utf8'))}
	return {'statut': 400, 'msg': "Les références inférieures à 98500 ne sont pas encore disponible."}


@bp.route('/stockage/<apikey>', methods = ['POST'])
@api_auth_required
def stockage(apikey): # Enregistrement.
	try :
		req_data = request.get_json(force=True)
		image = req_data['img']
	except Exception as e :
		return {'statut': 400, 'msg': "Aucune donnée associée à cette requete."}
	import base64, re
	from aip import AipOcr
	imagebyte = base64.b64decode(image)
	Xop = AipOcr('15536930','1afN81Kiwy5bGIfy3jGBGIDU','w6OXaech6MN4Vs07X96NqqvKal0DGGPa')
	datas = Xop.basicAccurate(imagebyte)
	number = datas['words_result_num']
	extraitcode = "{}{}".format(datas['words_result'][number-2]['words'], datas['words_result'][number-1]['words'])
	codequittance = re.sub(r'(\d{4})', r'\1 ', extraitcode).strip()
	SQL = "SELECT refcmd, ordre FROM quittances WHERE codequittance = '{}'".format(codequittance)
	quittance = medoo.query(SQL, True)
	if quittance is None :
		filename = 'IA{}.jpg'.format(datas['words_result'][1]['words'])
		filename = os.path.join(rootapp, "uittanx", "mixte", filename)
	else :
		filename = '{}.jpg'.format(quittance[0] if quittance[1] == 1 else '{}_{}'.format(quittance[0],quittance[1]))
		filename = os.path.join(rootapp, "uittanx", "psbee", filename)
	with open(filename, 'wb') as img :
		img.write(imagebyte)
	return {'statut': 200, 'msg': "L'enregistrement de la quittance reçu est un succès."}
