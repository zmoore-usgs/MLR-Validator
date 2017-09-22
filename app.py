import os

from flask import Flask

from mlrvalidator.site_file_validator_rules import SitefileValidator
from mlrvalidator.site_file_validator_warnings import SitefileWarningValidator


application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

sitefile_insert_error_validator = SitefileValidator()
sitefile_insert_error_validator.allow_unknown = True

sitefile_insert_warning_validator = SitefileWarningValidator()
sitefile_insert_warning_validator.allow_unknown = True

from mlrvalidator.services import *

if __name__ == '__main__':
    application.run()