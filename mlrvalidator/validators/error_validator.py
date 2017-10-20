
from collections import defaultdict
from itertools import chain
import os
import yaml

from app import application

from .single_field_validator import SingleFieldValidator


class ErrorValidator:

    def __init__(self):
        with open(os.path.join(application.config['SCHEMA_DIR'], 'error_schema.yml')) as fd:
            error_schema = yaml.load(fd.read())

        self.single_field_validator = SingleFieldValidator(error_schema, allow_unknown=True)
        self._errors = defaultdict(list)

    def validate(self, ddot_location, existing_location, update=False):
        valid_single_field = self.single_field_validator.validate(ddot_location, update=update)
        self._errors = defaultdict(list)
        self._errors = self.single_field_validator.errors.items()

        return valid_single_field

    @property
    def errors(self):
        return self._errors

