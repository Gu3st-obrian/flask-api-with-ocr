import os
import sys
from flaskr import create_app

sys.path.insert(0, os.path.dirname(__file__))
app = create_app()
