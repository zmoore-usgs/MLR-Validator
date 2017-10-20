
from . import aquifer_reference, huc_reference, mcd_reference, national_aquifer_reference, \
    national_water_use_reference, reference_lists, county_reference, state_reference
from .base_cross_field_validator import BaseCrossFieldValidator


class ReferenceValidator(BaseCrossFieldValidator):

    def _is_not_in_list(self, value, ref_list, upper_flag):
        stripped_value = value.strip()
        if upper_flag == 'upper':
            stripped_value = stripped_value.upper()

        if stripped_value and stripped_value not in ref_list:
            return True
        else:
            return False


