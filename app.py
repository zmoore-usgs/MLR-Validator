import os

from flask import Flask

from mlrvalidator.validators.error_validator import ErrorValidator
from mlrvalidator.validators.single_field_warning_validator import SingleFieldWarningValidator
from mlrvalidator.schema import warning_schema

application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

error_validator = ErrorValidator()
warning_validator = SingleFieldWarningValidator(warning_schema, allow_unknown=True)


from mlrvalidator.services import *

if __name__ == '__main__':
    application.run()