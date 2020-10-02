import functools
from flask import Blueprint, render_template, url_for

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
	from datetime import datetime
	aujourdhui = '{:%d-%m-%Y %H:%M:%S}'.format(datetime.now())
	return render_template('default.html', aujourdhui = aujourdhui)