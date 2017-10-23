
from collections import defaultdict
from itertools import chain
import os
import yaml

from app import application

from .cross_field_error_validator import Cross_Field_Error_Validator
from .cross_field_ref_validator import  CrossFieldRefValidator
from .single_field_validator import SingleFieldValidator
from .transition_validator import TransitionValidator



class ErrorValidator:

    def __init__(self):
        with open(os.path.join(application.config['SCHEMA_DIR'], 'error_schema.yml')) as fd:
            error_schema = yaml.load(fd.read())

        self.single_field_validator = SingleFieldValidator(error_schema, allow_unknown=True)
        self._errors = []

    def validate(self, ddot_location, existing_location, update=False):
        self.single_field_validator.validate(ddot_location, update=update)

        return self._errors == []

    @property
    def errors(self):
        return self._errors

