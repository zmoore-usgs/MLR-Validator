import os

from flask import Flask

from mlrvalidator.site_file_validator_rules import SitefileValidator
from mlrvalidator.site_file_validator_warnings import SitefileWarningValidator
from mlrvalidator.site_file_reference_validator import SitefileReferenceValidator
from mlrvalidator.schema import single_field_schema, warning_schema, reference_schema


application = Flask(__name__)

application.config.from_object('config')

PROJECT_DIR = os.path.dirname(__file__)
if os.path.exists(os.path.join(PROJECT_DIR, '.env')):
    application.config.from_pyfile('.env')

sitefile_single_field_validator = SitefileValidator(single_field_schema)
sitefile_single_field_validator.allow_unknown = True

sitefile_reference_validator = SitefileReferenceValidator(reference_schema)
sitefile_reference_validator.allow_unknown = True

sitefile_warning_validator = SitefileWarningValidator(warning_schema)
sitefile_warning_validator.allow_unknown = True

from mlrvalidator.services import *

if __name__ == '__main__':
    application.run()