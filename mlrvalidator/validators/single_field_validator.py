
import datetime
import re

from cerberus import Validator

from .land_net_templates import land_net_ref


class SingleFieldValidator(Validator):
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

    def _validate_valid_precision(self, valid_precision, field, value):
        """
        # Check that precision is no more than 2 decimal places

        The rule's arguments are validated against this schema:
        {'valid_precision': False}
        """
        error_message = "Invalid Value, decimal precision error"

        stripped_value = value.strip()
        test_split = stripped_value.split(".", 1)
        # there is a decimal, so need to check what's after it
        if len(test_split) > 1:
            if test_split[1] == "":
                self._error(field, error_message)
            else:
                # Check that only digits 0-9 exist after the decimal
                test_field = re.search('[^0-9]+', test_split[1])
                if test_field is not None:
                    # There is something besides digits 0-9 after the decimal
                    self._error(field, error_message)
                if len(test_split[1]) > 2:
                    self._error(field, error_message)

    def _validate_is_empty(self, is_empty, field, value):
        """
        # Since the value coming in could consist of spaces, check that a value of only spaces is considered null

        The rule's arguments are validated against this schema:
        {'valid_is_empty': False}
        """
        stripped_value = value.strip()
        if not is_empty:
            if not stripped_value:
                self._error(field, "Field must contain non whitespace characters")

    def _validate_valid_site_number(self, valid_site_number, field, value):
        """
        # We are not validation format as specified in http://nwis.usgs.gov/nwisdocs4_3/gw/gwcoding_Sect2-1.pdf,
        however, need to ensure that the site number consists of only digits

        The rule's arguments are validated against this schema:
        {'valid_site_number': True}
        """
        stripped_value = value.strip()
        if valid_site_number and stripped_value:
            if not stripped_value.isdigit():
                self._error(field, "Site Number can only have digits 0-9")

    def _validate_valid_special_chars(self, valid_special_chars, field, value):
        """
        # Check that tab, #, *, \, ", ^, _, and $ do not exist in field

        The rule's arguments are validated against this schema:
        {'valid_special_chars': True}
        """
        if valid_special_chars:
            test_field = re.search(r'[\t#*\\\"^_$]+', value)
            if test_field is not None:
                self._error(field, "Invalid Character: contains tab, #, *, \, "", ^, _, or $")

    def _validate_valid_map_scale_chars(self, valid_map_scale_chars, field, value):
        """
        # Check that characters other than 0-9 or a blank space do not exist in field

        The rule's arguments are validated against this schema:
        {'valid_map_scale_chars': True}
        """
        if valid_map_scale_chars:
            test_field = re.search('[^0-9 ]+', value)
            if test_field is not None:
                # There is something besides digits 0-9 or space
                self._error(field, "Invalid Character: contains a character other than 0-9")

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
        error_message = "Invalid Degree/Minute/Second Value"
        rstripped_value = value.rstrip()

        def check_100th_seconds(val):
            try:
                if val[7] in ["."]:
                    test_split = val.split(".")
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
                else:
                    return False
            except IndexError:
                return True

        if valid_latitude_dms and rstripped_value:
            first_val = rstripped_value[0]
            check_degrees = rstripped_value[1:3]
            check_minutes = rstripped_value[3:5]
            check_seconds = rstripped_value[5:7]

            try:
                if not ((first_val in "- ") and (0 <= int(check_degrees) <= 90) and (
                        0 <= int(check_minutes) < 60) and (0 <= int(check_seconds) < 60)
                        and check_100th_seconds(rstripped_value)):
                    self._error(field, error_message)
            except ValueError:
                return self._error(field, error_message)

    def _validate_valid_longitude_dms(self, valid_longitude_dms, field, value):
        # Check that field consists of valid degrees, minutes and second values

        """
        The rule's arguments are validated against this schema:
        {'valid_longitude_dms': True}
        """
        error_message = "Invalid Degree/Minute/Second Value"
        rstripped_value = value.rstrip()

        def check_100th_seconds(val):
            try:
                if val[8] in ["."]:
                    test_split = val.split(".")
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
                else:
                    return False
            except IndexError:
                return True

        if valid_longitude_dms and rstripped_value:
            first_val = rstripped_value[0]
            check_degrees = rstripped_value[1:4]
            check_minutes = rstripped_value[4:6]
            check_seconds = rstripped_value[6:8]
            try:
                if not ((first_val in "- ") and (0 <= int(check_degrees) <= 180) and (
                        0 <= int(check_minutes) < 60) and (0 <= int(check_seconds) < 60)
                        and check_100th_seconds(rstripped_value)):
                    self._error(field, error_message)
            except ValueError:
                return self._error(field, error_message)

    def _validate_valid_date(self, valid_date, field, value):
        # Check that field is a formatted date of YYYY, YYYYMM or YYYYMMDD

        """
        The rule's arguments are validated against this schema:
        {'valid_date': True}
        """
        error_message = "Invalid Date, should be YYYY, YYYYMM or YYYYMMDD"
        stripped_value = value.strip()
        if valid_date:
        # Check for valid full or partial date lengths
            if len(stripped_value) in [8, 6, 4]:
                # Check that only digits 0-9 exist in the string
                test_field = re.search('[^0-9]+', stripped_value)
                if test_field is None:
                    # There are only digits 0-9 in the string
                    check_year = stripped_value[0:4]
                    check_month = stripped_value[4:6]
                    if not 1582 <= int(check_year) <= int(datetime.date.today().year):
                        self._error(field, error_message)
                    if len(stripped_value) == 8:
                        try:
                            valid_date = datetime.datetime.strptime(stripped_value, '%Y%m%d')
                        except ValueError:
                            return self._error(field, error_message)
                    if check_month:
                        if not 1 <= int(check_month) <= 12:
                            self._error(field, error_message)

                else:
                    self._error(field, error_message)
            else:
                self._error(field, error_message)

    def _validate_valid_land_net(self, valid_land_net, field, value):
        # Check that the land net description field follows the correct template

        """
        The rule's arguments are validated against this schema:
        {'valid_land_net': True}
        """
        error_message = "Invalid format - Land Net does not fit template"

        if valid_land_net:
            land_net_template = land_net_ref["55"]
            value_end = len(value) - 1
            section = land_net_template.index("S")
            township = land_net_template.index("T")
            range = land_net_template.index("R")
            try:
                if not (value[section] == "S" and value[township] == "T" and value[range] == "R"):
                    return self._error(field, error_message)
                test_match = re.search('[^a-zA-Z0-9 ]', value[section:value_end])
                if test_match is not None:
                    return self._error(field, error_message)
            except IndexError:
                return self._error(field, error_message)
