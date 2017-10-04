
import re
from cerberus import Validator
from .reference import get_county_attributes, get_state_attributes


class SitefileWarningValidator(Validator):
    def _validate_valid_quotes(self, valid_quotes, field, value):
        """
        # Check for a single quote at the beginning at end of the incoming string

        The rule's arguments are validated against this schema:
        {'valid_quotes': True}
        """
        if valid_quotes:
            if ((value.startswith("'") and not value.endswith("'")) or
                    (not value.startswith("'") and value.endswith("'"))):
                # There is something besides digits 0-9 or space
                self._error(field, "Missing Quote: may be missing a quote at beginning or ending of the name")

    def _validate_valid_county_range(self, valid_county_range, field, value):
        """
        #  validate that the selected county is in range of the bounding latitude and longitude

        The rule's arguments are validated against this schema:
        {'valid_county_range': True}
        """

        if valid_county_range and self.document['countryCode'].upper() == 'US':

            county_attributes = get_county_attributes(self.document['countryCode'].upper(),
                                                      self.document['stateFipsCode'], value)
            if county_attributes and county_attributes['county_min_lat_va'] and county_attributes['county_max_lat_va']:
                if not float(county_attributes['county_min_lat_va']) <= float(self.document['latitude']) <= float(county_attributes['county_max_lat_va']):
                    return self._error(field, "Latitude Out of Range")

            if county_attributes and county_attributes['county_min_long_va'] and county_attributes['county_max_long_va']:
                if not float(county_attributes['county_min_long_va']) <= float(self.document['longitude']) <= float(county_attributes['county_max_long_va']):
                    return self._error(field, "Longitude Out of Range")

    def _validate_valid_state_range(self, valid_state_range, field, value):
        """
        #  validate that the selected state is in range of the bounding latitude and longitude

        The rule's arguments are validated against this schema:
        {'valid_state_range': True}
        """

        if valid_state_range and self.document['countryCode'].upper() == 'US':

            state_attributes = get_state_attributes(self.document['countryCode'].upper(), value)
            if state_attributes and state_attributes['state_min_lat_va'] and state_attributes['state_max_lat_va']:
                if not float(state_attributes['state_min_lat_va']) <= float(self.document['latitude']) <= float(state_attributes['state_max_lat_va']):
                    return self._error(field, "Latitude Out of Range")

            if state_attributes and state_attributes['state_min_long_va'] and state_attributes['state_max_long_va']:
                if not float(state_attributes['state_min_long_va']) <= float(self.document['longitude']) <= float(state_attributes['state_max_long_va']):
                    return self._error(field, "Longitude Out of Range")

    def _validate_valid_altitude_range(self, valid_altitude_range, field, value):
        """
        #  validate that the altitude is in the allowable alitude range of the selected state

        The rule's arguments are validated against this schema:
        {'valid_altitude_range': True}
        """
        stripped_value = value.strip()

        if valid_altitude_range and stripped_value:
            state_attributes = get_state_attributes(self.document['countryCode'].upper(), self.document['stateFipsCode'])

            if state_attributes and state_attributes['state_min_alt_va'] and state_attributes['state_max_alt_va']:
                stripped_min = re.split(".(?=-)", state_attributes['state_min_alt_va'])
                stripped_max = re.split(".(?=-)", state_attributes['state_max_alt_va'])
                min_alt_va = stripped_min[len(stripped_min) - 1]
                max_alt_va = stripped_max[len(stripped_max) - 1]
                if not float(min_alt_va) <= float(value) <= float(max_alt_va):
                    return self._error(field, "Altitude Out of Range for State")
