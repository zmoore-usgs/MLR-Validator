from collections import defaultdict
from itertools import chain
import os
import yaml

from .cross_field_ref_warning_validator import CrossFieldRefWarningValidator
from .cross_field_warning_validator import CrossFieldWarningValidator
from .single_field_validator import SingleFieldValidator

class WarningValidator:

    def __init__(self, schema_dir, parent_reference_file_dir):
        with open(os.path.join(schema_dir, 'warning_schema.yml')) as fd:
            warning_schema = yaml.full_load(fd.read())
        remote_reference_dir = os.path.join(parent_reference_file_dir, 'remote')
        self.single_field_validator = SingleFieldValidator(warning_schema, parent_reference_dir=parent_reference_file_dir, allow_unknown=True)
        self.cross_field_ref_validator = CrossFieldRefWarningValidator(remote_reference_dir)
        self.cross_field_validator = CrossFieldWarningValidator()
        self._warnings = defaultdict(list)

    def validate(self, ddot_location, existing_location, update=False):
        self.single_field_validator.validate(ddot_location, update=update)
        self.cross_field_ref_validator.validate(ddot_location, existing_location)
        self.cross_field_validator.validate(ddot_location, existing_location)

        self._warnings = defaultdict(list)
        all_warnings = chain(self.single_field_validator.errors.items(),
                             self.cross_field_ref_validator.errors.items(),
                             self.cross_field_validator.errors.items())

        for k, v in chain(all_warnings):
            self._warnings[k].extend(v)

        return self._warnings == {}

    @property
    def warnings(self):
        return self._warnings