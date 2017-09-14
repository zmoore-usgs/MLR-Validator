from cerberus import Validator
import re

class SitefileValidator(Validator):
    def _validate_type_numeric(self, value):
        # check for numeric value
        try:
            float(value)
        except ValueError:
            return False

        return True

    def _validate_type_positive_numeric(self, value):
        # check for positive numeric value
        try:
            test_num = float(value)
        except ValueError:
            return False

        if test_num < 0:
            return False
        else:
            return True

    def _validate_valid_chars(self, valid_chars, field, value):
        """
        # Check that tab, #, *, \, ", ^, _, and $ do not exist in field

        The rule's arguments are validated against this schema:
        {'valid_chars': True}
        """
        if valid_chars:
            if field == 'stationName':
                test_field = re.search('[\\t\#\*\\\\"\^\_\$]+', value)
                if test_field is not None:
                    self._error(field, "Invalid Character: contains tab, #, *, \, "", ^, _, and $")
            elif field == 'instrumentsCode':
                if not all(c.upper() in "YN " for c in value):
                    self._error(field, "Invalid Character: contains a character other than Y, N, or a blank space")
            elif field == 'dataTypesCode':
                if not all(c.upper() in "AION " for c in value):
                    self._error(field, "Invalid Character: contains a character other than A, I, O, N, or a blank space")

    def _validate_valid_dms(self, valid_dms, field, value):
        # Check that field consists of valid degrees, minutes and second values

        """
        The rule's arguments are validated against this schema:
        {'valid_chars': True}
        """
        if valid_dms:
            if field == 'latitude':
                first_val = value[0]
                check_degrees = value[1:3]
                check_minutes = value[3:5]
                check_seconds = value[5:7]
                if not check_degrees.isnumeric() or not check_minutes.isnumeric or not check_seconds.isnumeric or not (
                    first_val in "- ") or not (0 <= int(check_degrees) <= 90) or not (
                        0 <= int(check_minutes) <= 60) or not (0 <= int(check_seconds) <= 60):
                    self._error(field, "Invalid Degree/Minute/Second Value")


class ValidateError(Exception):
    def __init__(self, message):
        self.message = message


def validate(data, schema):
    '''

    :param data:
    :param schema:
    :return: boolean True if validation successful
    :raises: ValidateError with an appropriate message if unable to validate data.
    '''

    v = SitefileValidator()
    v.allow_unknown = True
    result = v.validate(data, schema)

    if not result:
        raise ValidateError('Validation Error: {0}'.format(v.errors))

    return 'Validation Successful'
