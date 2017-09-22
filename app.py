import os

from flask import Flask

from .site_file_validator_rules import SitefileValidator


application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

sitefile_validator = SitefileValidator()
sitefile_validator.allow_unknown = True

from .services import *

if __name__ == '__main__':
    application.run()