import os

from flask import Flask
import requests

from mlrvalidator.validators.error_validator import ErrorValidator
from mlrvalidator.validators.warning_validator import WarningValidator

application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

if application.config.get('AUTH_TOKEN_KEY_URL'):
    resp = requests.get(application.config.get('AUTH_TOKEN_KEY_URL'), verify=application.config['AUTH_CERT_PATH'])
    application.config['JWT_PUBLIC_KEY'] = resp.json()['value']
    application.config['JWT_ALGORITHM'] = 'RS256'

error_validator = ErrorValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])
warning_validator = WarningValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])


from mlrvalidator.services import *

if __name__ == '__main__':
    application.run()