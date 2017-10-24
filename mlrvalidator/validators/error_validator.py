
from collections import defaultdict
from itertools import chain
import os
import yaml

from app import application

from .cross_field_error_validator import CrossFieldErrorValidator
from .cross_field_ref_error_validator import CrossFieldRefErrorValidator
from .single_field_validator import SingleFieldValidator
from .transition_validator import TransitionValidator


class ErrorValidator:

    def __init__(self):
        with open(os.path.join(application.config['SCHEMA_DIR'], 'error_schema.yml')) as fd:
            error_schema = yaml.load(fd.read())

        self.single_field_validator = SingleFieldValidator(error_schema, allow_unknown=True)
        self.cross_field_validator = CrossFieldErrorValidator()
        self.cross_field_ref_validator = CrossFieldRefErrorValidator(application.config['REFERENCE_FILE_DIR'])
        self.transition_validator = TransitionValidator(application.config['REFERENCE_FILE_DIR'])
        self._errors = defaultdict(list)

    def validate(self, ddot_location, existing_location, update=False):
        self.single_field_validator.validate(ddot_location, update=update)
        self.cross_field_validator.validate(ddot_location, existing_location)
        self.cross_field_ref_validator.validate(ddot_location, existing_location)

        if update:
            self.transition_validator.validate(ddot_location, existing_location)
            transition_errors = self.transition_validator.errors
        else:
            transition_errors = {}

        self._errors = defaultdict(list)
        all_errors = chain(self.single_field_validator.errors.items(),
                           self.cross_field_validator.errors.items(),
                           self.cross_field_ref_validator.errors.items(),
                           transition_errors.items())

        for k, v in chain(all_errors):
            self.errors[k].extend(v)
        return self._errors == {}

    @property
    def errors(self):
        return self._errors

