from collections import defaultdict
from itertools import chain
import os
import yaml

from .cross_field_ref_warning_validator import CrossFieldRefWarningValidator
from .single_field_validator import SingleFieldValidator

class WarningValidator:

    def __init__(self, schema_dir, reference_file_dir):
        with open(os.path.join(schema_dir, 'warning_schema.yml')) as fd:
            warning_schema = yaml.load(fd.read())

        self.single_field_validator = SingleFieldValidator(warning_schema, reference_dir=reference_file_dir, allow_unknown=True)
        self.cross_field_ref_validator = CrossFieldRefWarningValidator(reference_file_dir)
        self._warnings = defaultdict(list)

    def validate(self, ddot_location, existing_location, update=False):
        self.single_field_validator.validate(ddot_location, update=update)
        self.cross_field_ref_validator.validate(ddot_location, existing_location)

        self._errors = defaultdict(list)
        all_warnings = chain(self.single_field_validator.errors.items(),
                             self.cross_field_ref_validator.errors.items())

        for k, v in chain(all_warnings):
            self._warnings[k].extend(v)

        return self._warnings == {}

    @property
    def warnings(self):
        return self._warnings