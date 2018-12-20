
from collections import defaultdict
from itertools import chain
import os
import yaml

from .cross_field_error_validator import CrossFieldErrorValidator
from .cross_field_ref_error_validator import CrossFieldRefErrorValidator
from .single_field_validator import SingleFieldValidator
from .transition_validator import TransitionValidator


class ErrorValidator:

    def __init__(self, schema_dir, reference_file_dir):
        with open(os.path.join(schema_dir, 'error_schema.yml')) as fd:
            error_schema = yaml.load(fd.read())

        self.single_field_validator = SingleFieldValidator(error_schema, reference_dir=reference_file_dir, allow_unknown=True)
        self.cross_field_validator = CrossFieldErrorValidator()
        self.cross_field_ref_validator = CrossFieldRefErrorValidator(reference_file_dir)
        self.transition_validator = TransitionValidator(reference_file_dir)
        self._errors = defaultdict(list)

    def validate(self, ddot_location, existing_location, update=False):
        """
        Validates location creations and updates

        :param ddot_location: dict describing properties of a new location or properties to be merged into an existing location
        :param existing_location: dict describing properties of an existing location. Cannot be None, even if there is no existing location. Specify an empty dict instead.
        :param update: Boolean True if the properties in ddot_location should be merged into existing_location. False otherwise.
                        If this is False and existing_location is non-empty, this method returns False because it is considered a duplicate
        :return: Boolean True if valid, False if invalid.
        """
        self.single_field_validator.validate(ddot_location, update=update)
        self.cross_field_validator.validate(ddot_location, existing_location)
        self.cross_field_ref_validator.validate(ddot_location, existing_location)

        if update:
            self.transition_validator.validate(ddot_location, existing_location)
            transition_errors = self.transition_validator.errors
        else:
            transition_errors = {}

        self._errors = defaultdict(list)
        all_errors = chain(
            self.single_field_validator.errors.items(),
            self.cross_field_validator.errors.items(),
            self.cross_field_ref_validator.errors.items(),
            transition_errors.items(),
        )

        for k, v in chain(all_errors):
            self.errors[k].extend(v)
        return self._errors == {}

    @property
    def errors(self):
        return self._errors

