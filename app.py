import os

from flask import Flask

from mlrvalidator.validators.error_validator import ErrorValidator
from mlrvalidator.validators.warning_validator import WarningValidator

application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

error_validator = ErrorValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])
warning_validator = WarningValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])


from mlrvalidator.services import *

if __name__ == '__main__':
    application.run()