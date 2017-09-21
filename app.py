import os
from site_file_validator_rules import SitefileValidator
from site_file_validator_warnings import SitefileWarningValidator

from flask import Flask

application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

sitefile_validator = SitefileValidator()
sitefile_validator.allow_unknown = True
sitefile_warning_validator = SitefileWarningValidator()
sitefile_warning_validator.allow_unknown = True

from services import *

if __name__ == '__main__':
    application.run()