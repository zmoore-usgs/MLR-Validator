
from cerberus import Validator

from .reference import reference_lists, get_aquifers, get_national_aquifers, get_hucs, get_mcds, \
    get_national_water_use_codes, get_county_codes, get_state_codes, get_state_attributes


class SitefileReferenceValidator(Validator):
    def _validate_valid_reference(self, valid_reference, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_reference': True}
        """
        error_message = "Value not in reference list"
        stripped_value = value.strip()

        if valid_reference:
            ref_list = reference_lists[field]

            if stripped_value and stripped_value.upper() not in ref_list:
                return self._error(field, error_message)

    def _validate_valid_aquifer_code(self, valid_aquifer_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_aquifer_code': True}
        """
        error_message = "Value not in reference list"

        if valid_aquifer_code:
            stripped_value = value.strip()

            aquifer_list = get_aquifers(self.document['countryCode'].upper(), self.document['stateFipsCode'])

            if not aquifer_list:
                return self._error(field, error_message)

            if stripped_value and stripped_value.upper() not in aquifer_list:
                return self._error(field, error_message)

    def _validate_valid_national_aquifer_code(self, valid_national_aquifer_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_national_aquifer_code': True}
        """
        error_message = "Value not in reference list"

        if valid_national_aquifer_code:
            stripped_value = value.strip()

            national_aquifer_list = get_national_aquifers(self.document['countryCode'].upper(), self.document['stateFipsCode'])

            if not national_aquifer_list:
                return self._error(field, error_message)

            if stripped_value and stripped_value.upper() not in national_aquifer_list:
                return self._error(field, error_message)

    def _validate_valid_huc(self, valid_huc, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_huc': True}
        """
        error_message = "Value not in reference list"

        if valid_huc:
            stripped_value = value.strip()

            huc_list = get_hucs(self.document['countryCode'].upper(), self.document['stateFipsCode'])

            if not huc_list:
                return self._error(field, error_message + "--Hydrologic units do not exist in the HUC reference list for the entered State Code")

            if stripped_value != '99999999' and stripped_value and stripped_value not in huc_list:
                return self._error(field, error_message)

    def _validate_valid_mcd_code(self, valid_mcd_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_mcd_code': True}
        """
        error_message = "Value not in reference list"

        if valid_mcd_code:
            stripped_value = value.strip()

            mcd_list = get_mcds(self.document['countryCode'].upper(), self.document['stateFipsCode'])

            if not mcd_list:
                return self._error(field, error_message)

            if stripped_value and stripped_value.upper() not in mcd_list:
                return self._error(field, error_message)

    def _validate_valid_national_water_use_code(self, valid_national_water_use_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_valid_national_water_use_code': True}
        """
        error_message = "Value not in reference list"

        if valid_national_water_use_code:
            stripped_value = value.strip()

            national_water_use_code_list = get_national_water_use_codes(self.document['siteTypeCode'].upper())

            if not national_water_use_code_list:
                return self._error(field, error_message)

            if stripped_value and stripped_value.upper() not in national_water_use_code_list:
                return self._error(field, error_message)

    def _validate_valid_county_code(self, valid_county_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_county_code': True}
        """
        error_message = "Value not in reference list"

        if valid_county_code:
            stripped_value = value.strip()

            county_list = get_county_codes(self.document['countryCode'].upper(), self.document['stateFipsCode'])

            if not county_list:
                return self._error(field, error_message)

            if stripped_value and stripped_value.upper() not in county_list:
                return self._error(field, error_message)

    def _validate_valid_state_code(self, valid_state_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_state_code': True}
        """
        error_message = "Value not in reference list"

        if valid_state_code:
            stripped_value = value.strip()

            state_list = get_state_codes(self.document['countryCode'].upper())

            if not state_list:
                return self._error(field, error_message)

            if stripped_value and stripped_value.upper() not in state_list:
                return self._error(field, error_message)

