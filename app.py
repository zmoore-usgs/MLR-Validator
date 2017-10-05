import os

from flask import Flask

from mlrvalidator.site_file_validator_rules import SitefileValidator
from mlrvalidator.site_file_validator_warnings import SitefileWarningValidator
from mlrvalidator.site_file_cross_field_validator_rules import CrossFieldValidator
from mlrvalidator.schema import error_schema, warning_schema, cross_field_schema


application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

sitefile_error_validator = SitefileValidator(error_schema)
sitefile_error_validator.allow_unknown = True

sitefile_warning_validator = SitefileWarningValidator(warning_schema)
sitefile_warning_validator.allow_unknown = True

sitefile_crossfield_error_validator = CrossFieldValidator(cross_field_schema)
sitefile_crossfield_error_validator.allow_unknown = True

from mlrvalidator.services import *

if __name__ == '__main__':
    application.run()