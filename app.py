import os
from site_file_validator import SitefileValidator

from flask import Flask

application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

from services import *

v = SitefileValidator()
v.allow_unknown = True

if __name__ == '__main__':
    application.run()