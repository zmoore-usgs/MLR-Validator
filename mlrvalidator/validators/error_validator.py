
from collections import defaultdict
from itertools import chain

from mlrvalidator.schema import single_field_schema, cross_field_schema, reference_schema, site_type_cross_field_schema

from .cross_field_validator import CrossFieldValidator
from .single_field_validator import SingleFieldValidator
from .site_type_cross_field_validator import SiteTypeCrossFieldValidator
from .reference_validator import ReferenceValidator


class ErrorValidator:

    def __init__(self):
        self.single_field_validator = SingleFieldValidator(single_field_schema, allow_unknown=True)
        self.reference_validator = ReferenceValidator(reference_schema, allow_unknown=True)
        self.site_type_cross_field_validator = SiteTypeCrossFieldValidator(site_type_cross_field_schema, allow_unknown=True)
        self.cross_field_validator = CrossFieldValidator(cross_field_schema, allow_unknown=True)
        self._errors = defaultdict(list)

    def validate(self, ddot_location, existing_location, update=False):
        valid_single_field = self.single_field_validator.validate(ddot_location, update=update)
        valid_reference = self.reference_validator.validate(ddot_location, existing_location, update=update)
        valid_site_type = self.site_type_cross_field_validator.validate(ddot_location, existing_location, update=update)
        valid_cross_field = self.cross_field_validator.validate(ddot_location, existing_location, update=update)

        self._errors = defaultdict(list)
        all_errors = chain(self.single_field_validator.errors.items(),
                       self.reference_validator.errors.items(),
                       self.site_type_cross_field_validator.errors.items(),
                       self.cross_field_validator.errors.items())
        for k, v in all_errors:
            self.errors[k].extend(v)

        return valid_single_field and valid_reference and valid_site_type and valid_cross_field

    @property
    def errors(self):
        return self._errors
