
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

    def _validate_valid_reference(self, valid_reference, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_reference': True}
        """
        error_message = "Value not in reference list"

        if valid_reference:
            ref_list = reference_lists.reference_info[field]

            if self._is_not_in_list(value, ref_list, 'upper'):
                return self._error(field, error_message)

    def _validate_valid_aquifer_code(self, valid_aquifer_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_aquifer_code': True}
        """
        error_message = "Value not in reference list"

        if valid_aquifer_code:
            aquifer_list = aquifer_reference.get_aquifers(
                self.merged_document.get('countryCode', '').upper(),
                self.merged_document.get('stateFipsCode', '')
            )

            if not aquifer_list:
                return self._error(field, error_message)

            if self._is_not_in_list(value, aquifer_list, 'upper'):
                return self._error(field, error_message)

    def _validate_valid_national_aquifer_code(self, valid_national_aquifer_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_national_aquifer_code': True}
        """
        error_message = "Value not in reference list"

        if valid_national_aquifer_code:
            national_aquifer_list = national_aquifer_reference.get_national_aquifers(
                self.merged_document.get('countryCode', '').upper(),
                self.merged_document.get('stateFipsCode', '')
            )

            if not national_aquifer_list:
                return self._error(field, error_message)

            if self._is_not_in_list(value, national_aquifer_list, 'upper'):
                return self._error(field, error_message)

    def _validate_valid_huc(self, valid_huc, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_huc': True}
        """
        error_message = "Value not in reference list"

        if valid_huc:
            huc_list = huc_reference.get_hucs(
                self.merged_document.get('countryCode', '').upper(),
                self.merged_document.get('stateFipsCode', '')
            )

            if not huc_list:
                return self._error(field, error_message + "--Hydrologic units do not exist in the HUC reference list for the entered State Code")

            if value.strip() != '99999999' and self._is_not_in_list(value, huc_list, ''):
                return self._error(field, error_message)

    def _validate_valid_mcd_code(self, valid_mcd_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_mcd_code': True}
        """
        error_message = "Value not in reference list"

        if valid_mcd_code:
            mcd_list = mcd_reference.get_mcds(
                self.merged_document.get('countryCode', '').upper(),
                self.merged_document.get('stateFipsCode', '')
            )

            if not mcd_list:
                return self._error(field, error_message)

            if self._is_not_in_list(value, mcd_list, 'upper'):
                return self._error(field, error_message)

    def _validate_valid_national_water_use_code(self, valid_national_water_use_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_valid_national_water_use_code': True}
        """
        error_message = "Value not in reference list"

        if valid_national_water_use_code:
            national_water_use_code_list = national_water_use_reference.get_national_water_use_codes(
                self.merged_document.get('siteTypeCode', '').upper()
            )

            if not national_water_use_code_list:
                return self._error(field, error_message)

            if self._is_not_in_list(value, national_water_use_code_list, 'upper'):
                return self._error(field, error_message)

    def _validate_valid_county_code(self, valid_county_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_county_code': True}
        """
        error_message = "Value not in reference list"

        if valid_county_code:
            county_list = county_reference.get_county_codes(
                self.merged_document.get('countryCode', '').upper(),
                self.merged_document.get('stateFipsCode', '')
            )

            if not county_list:
                return self._error(field, error_message)

            if self._is_not_in_list(value, county_list, 'upper'):
                return self._error(field, error_message)

    def _validate_valid_state_code(self, valid_state_code, field, value):
        """
        # Check that value is the list of allowable values

        The rule's arguments are validated against this schema:
        {'valid_state_code': True}
        """
        error_message = "Value not in reference list"

        if valid_state_code:
            state_list = state_reference.get_state_codes(
                self.merged_document.get('countryCode','').upper()
            )

            if not state_list:
                return self._error(field, error_message)

            if self._is_not_in_list(value, state_list, 'upper'):
                return self._error(field, error_message)

