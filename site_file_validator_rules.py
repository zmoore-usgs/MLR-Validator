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

    def _validate_valid_special_chars(self, valid_special_chars, field, value):
        """
        # Check that tab, #, *, \, ", ^, _, and $ do not exist in field

        The rule's arguments are validated against this schema:
        {'valid_special_chars': True}
        """
        if valid_special_chars:
            test_field = re.search('[\\t#*\\\\\"^_$]+', value)
            if test_field is not None:
                self._error(field, "Invalid Character: contains tab, #, *, \, "", ^, _, and $")

    def _validate_valid_instruments_chars(self, valid_instruments_chars, field, value):
        """
        # Check that characters other than Y, N, or a blank space do not exist in field

        The rule's arguments are validated against this schema:
        {'valid_instruments_chars': True}
        """
        if valid_instruments_chars:
            if not all(c.upper() in "YN " for c in value):
                self._error(field, "Invalid Character: contains a character other than Y, N, or a blank space")

    def _validate_valid_data_types_chars(self, valid_data_types_chars, field, value):
        """
        # Check that character other than A, I, O, N, or a blank space do not exist in field

        The rule's arguments are validated against this schema:
        {'valid_data_types_chars': True}
        """
        if valid_data_types_chars:
            if not all(c.upper() in "AION " for c in value):
                self._error(field, "Invalid Character: contains a character other than A, I, O, N, or a blank space")

    def _validate_valid_latitude_dms(self, valid_latitude_dms, field, value):
        # Check that field consists of valid degrees, minutes and second values

        """
        The rule's arguments are validated against this schema:
        {'valid_latitude_dms': True}
        """
        def check_100th_seconds(val):
            try:
                val[7] in ["."]
                test_split = val.split(".")
                if len(test_split) == 1:
                    # no 100th second decimal to check, we're all good
                    return True
                else:
                    # There is a decimal, but have to check if anything was split from it
                    if test_split[1] == "":
                        return False
                    else:
                        # Check that only digits 0-9 exist after the decimal
                        test_field = re.search('[^0-9]+', test_split[1])
                        if test_field is None:
                            # There are only digits 0-9 after the decimal
                            return True
                        else:
                            # There is something besides digits 0-9 after the decimal
                            return False
            except IndexError:
                return True

        if valid_latitude_dms:
            first_val = value[0]
            check_degrees = value[1:3]
            check_minutes = value[3:5]
            check_seconds = value[5:7]

            try:
                if not ((first_val in "- ") and (0 <= int(check_degrees) <= 90) and (
                        0 <= int(check_minutes) < 60) and (0 <= int(check_seconds) < 60)
                        and check_100th_seconds(value)):
                    self._error(field, "Invalid Degree/Minute/Second Value")
            except ValueError:
                return self._error(field, "Invalid Degree/Minute/Second Value")
            except IndexError:
                return

    def _validate_valid_longitude_dms(self, valid_longitude_dms, field, value):
        # Check that field consists of valid degrees, minutes and second values

        """
        The rule's arguments are validated against this schema:
        {'valid_longitude_dms': True}
        """
        def check_100th_seconds(val):
            try:
                val[8] in ["."]
                test_split = val.split(".")
                if len(test_split) == 1:
                    # no 100th second decimal to check, we're all good
                    return True
                else:
                    # There is a decimal, but have to check if anything was split from it
                    if test_split[1] == "":
                        return False
                    else:
                        # Check that only digits 0-9 exist after the decimal
                        test_field = re.search('[^0-9]+', test_split[1])
                        if test_field is None:
                            # There are only digits 0-9 after the decimal
                            return True
                        else:
                            # There is something besides digits 0-9 after the decimal
                            return False
            except IndexError:
                return True

        if valid_longitude_dms:
            first_val = value[0]
            check_degrees = value[1:4]
            check_minutes = value[4:6]
            check_seconds = value[6:8]
            try:
                if not ((first_val in "- ") and (0 <= int(check_degrees) <= 180) and (
                        0 <= int(check_minutes) < 60) and (0 <= int(check_seconds) < 60)
                        and check_100th_seconds(value)):
                    self._error(field, "Invalid Degree/Minute/Second Value")
            except ValueError:
                return self._error(field, "Invalid Degree/Minute/Second Value")