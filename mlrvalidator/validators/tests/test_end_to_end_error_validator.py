
from unittest import TestCase

from app import application
from ..error_validator import ErrorValidator

validator = ErrorValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])


class ErrorValidatorAgencyCodeTestCase(TestCase):
    # We are leaving out the landNet validations for now as there too many questions as to how these will work
    # The existing land net validation is also well tested by unit tests.

    def test_agency_code_no_padding_is_valid(self):
        self.assertTrue(validator.validate({'agencyCode': 'USGS'}, {}, update=True))

    def test_agency_code_padding_is_valid(self):
        self.assertTrue(validator.validate({'agencyCode': 'USGS '}, {}, update=True))

    def test_agency_code_lower_padding_is_invalid(self):
        self.assertFalse(validator.validate({'agencyCode': 'usgs   '}, {}, update=True))

    def test_agency_code_lower_no_padding_is_invalid(self):
        self.assertFalse(validator.validate({'agencyCode': 'usgs'}, {}, update=True))

    def test_agency_code_not_in_ref_list_padding_is_invalid(self):
        self.assertFalse(validator.validate({'agencyCode': 'XYZ   '}, {}, update=True))

    def test_agency_code_not_in_ref_list_no_padding_is_invalid(self):
        self.assertFalse(validator.validate({'agencyCode': 'XYZ'}, {}, update=True))

    def test_agency_code_not_in_ref_list_padding_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'agencyCode': 'XYZ     '}, {}, update=True))
        self.assertEqual(len(validator.errors.get('agencyCode')), 2)

    def test_agency_code_in_ref_list_padding_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'agencyCode': 'USGS      '}, {}, update=True))
        self.assertEqual(len(validator.errors.get('agencyCode')), 1)

    def test_agency_code_null_is_invalid(self):
        self.assertFalse(validator.validate({'agencyCode': ''}, {}, update=True))
        self.assertEqual(len(validator.errors.get('agencyCode')), 1)

    def test_agency_code_null_padding_is_invalid(self):
        self.assertFalse(validator.validate({'agencyCode': ' '}, {}, update=True))
        self.assertEqual(len(validator.errors.get('agencyCode')), 1)

    def test_agency_code_padding_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'agencyCode': '           '}, {}, update=True))
        self.assertEqual(len(validator.errors.get('agencyCode')), 2)


class ErrorValidatorSiteNumberTestCase(TestCase):

    def test_only_digits_is_valid(self):
        self.assertTrue(validator.validate({'siteNumber': '01234'}, {}, update=True))

    def test_only_digits_trailing_space_is_valid(self):
        self.assertTrue(validator.validate({'siteNumber': '01234   '}, {}, update=True))

    def test_null_value_no_pad_is_invalid(self):
        self.assertFalse(validator.validate({'siteNumber': ''}, {}, update=True))
        self.assertEqual(len(validator.errors.get('siteNumber')), 1)

    def test_null_value_pad_is_invalid(self):
        self.assertFalse(validator.validate({'siteNumber': ' '}, {}, update=True))
        self.assertEqual(len(validator.errors.get('siteNumber')), 1)

    def test_non_digit_is_invalid(self):
        self.assertFalse(validator.validate({'siteNumber': 'a6'}, {}, update=True))

    def test_non_digit_special_char_is_invalid(self):
        self.assertFalse(validator.validate({'siteNumber': '$'}, {}, update=True))

    def test_only_digits_blank_space_is_invalid(self):
        self.assertFalse(validator.validate({'siteNumber': '32   4'}, {}, update=True))

    def test_only_digits_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'siteNumber': '0126954826512369548'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('siteNumber')), 1)

    def test_invalid_chars_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'siteNumber': '01269d82g651y23e69s548'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('siteNumber')), 2)

    def test_only_spaces_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'siteNumber': '                    '}, {}, update=True))
        self.assertEqual(len(validator.errors.get('siteNumber')), 2)


class ErrorValidatorStationNameTestCase(TestCase):

    def test_valid_chars_all_lower_is_valid(self):
        self.assertTrue(validator.validate({'stationName': 'br549'}, {}, update=True))

    def test_valid_chars_mix_upper_lower_is_valid(self):
        self.assertTrue(validator.validate({'stationName': 'YYyyNnNN'}, {}, update=True))

    def test_valid_chars_all_upper_is_valid(self):
        self.assertTrue(validator.validate({'stationName': 'ABCD'}, {}, update=True))

    def test_valid_chars_space_in_middle_is_valid(self):
        self.assertTrue(validator.validate({'stationName': 'br 549'}, {}, update=True))

    def test_allowed_special_chars_is_valid(self):
        self.assertTrue(validator.validate({'stationName': 'a-b'}, {}, update=True))

    def test_leading_space_is_valid(self):
        self.assertTrue(validator.validate({'stationName': '   BR549'}, {}, update=True))

    def test_trailing_space_is_valid(self):
        self.assertTrue(validator.validate({'stationName': 'BR549   '}, {}, update=True))

    def test_null_value_no_pad_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': ''}, {}, update=True))
        self.assertEqual(len(validator.errors.get('stationName')), 1)

    def test_null_value_pad_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': ' '}, {}, update=True))
        self.assertEqual(len(validator.errors.get('stationName')), 1)

    def test_bad_special_char_pound_sign_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': 'br5#49'}, {}, update=True))

    def test_bad_special_char_tab_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': 'br\t549'}, {}, update=True))

    def test_bad_special_char_backslash_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': 'br\\549'}, {}, update=True))

    def test_bad_special_char_dollar_sign_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': '$br549'}, {}, update=True))

    def test_bad_special_char_caret_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': 'b^r549'}, {}, update=True))

    def test_bad_special_char_asterisk_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': 'br5*49'}, {}, update=True))

    def test_bad_special_char_double_quotes_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': 'br54"9'}, {}, update=True))

    def test_bad_special_char_underscore_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': 'br549_'}, {}, update=True))

    def test_valid_chars_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': '0126954826512369548fesgdrs0126954826512369548fesgdrs'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('stationName')), 1)

    def test_invalid_chars_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': '01269d8#**2g65\\1y23e69s548                         '}, {}, update=True))
        self.assertEqual(len(validator.errors.get('stationName')), 2)

    def test_only_spaces_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'stationName': '                                                            '}, {}, update=True))
        self.assertEqual(len(validator.errors.get('stationName')), 2)


class ErrorValidatorLatitudeTestCase(TestCase):

    def test_null_no_pad_latitude_empty_string_dependencies_is_valid(self):
        self.assertTrue(validator.validate({'latitude': '', 'longitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                 'coordinateMethodCode': ''}, {}, update=True))

    def test_null_no_pad_latitude_dependencies_missing_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ''}, {}, update=True))

    def test_null_pad_latitude_dependencies_missing_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' '}, {}, update=True))

    def test_null_pad_latitude_pad_dependencies_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' ', 'longitude': ' ',
                                                 'coordinateAccuracyCode': ' ', 'coordinateDatumCode': ' ',
                                                 'coordinateMethodCode': ' '}, {}, update=True))

    def test_positive_dms_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_single_digit_degrees_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' 023456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' 003456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' 000456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' 000056', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' 000006', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' 000000', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' 905959', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(validator.validate({'latitude': ' 900000.0', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            validator.validate({'latitude': ' 900000.93', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            validator.validate({'latitude': ' 900000.093', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_is_valid(self):
        self.assertTrue(validator.validate({'latitude': '-123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_single_digit_degrees_is_valid(self):
        self.assertTrue(validator.validate({'latitude': '-023456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(validator.validate({'latitude': '-003456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(validator.validate({'latitude': '-000456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(validator.validate({'latitude': '-000056', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(validator.validate({'latitude': '-000006', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(validator.validate({'latitude': '-000000', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(validator.validate({'latitude': '-905959', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(validator.validate({'latitude': '-900000.0', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            validator.validate({'latitude': '-900000.93', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            validator.validate({'latitude': '-900000.093', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_seconds_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 9020', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_minutes_seconds_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 90', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_degrees_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 990000', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_minutes_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 207500', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_seconds_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 200066', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_too_many_seconds_decimals_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 200023.9234', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('latitude')), 1)

    def test_dangling_decimal_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 200023.', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('latitude')), 1)

    def test_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 20003234', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('latitude')), 1)

    def test_longer_than_maxlength_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 203300203234', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('latitude')), 2)

    def test_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': '             ', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('latitude')), 1)
        self.assertIn('latitude', validator.errors.get('location')[0])

    def test_latitude_without_longitude_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 040000',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('latitude', validator.errors.get('location')[0])

    def test_good_latitude_null_dependencies_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 123456', 'longitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('latitude', validator.errors.get('location')[0])

    def test_good_latitude_non_exist_dependencies_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 123456'}, {}, update=True))
        self.assertIn('latitude', validator.errors.get('location')[0])

    def test_good_latitude_good_longitude_null_dependencies_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('latitude', validator.errors.get('location')[0])

    def test_good_latitude_good_longitude_null_2_dependencies_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('latitude', validator.errors.get('location')[0])

    def test_good_latitude_good_longitude_null_1_dependency_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('latitude', validator.errors.get('location')[0])

    def test_first_char_not_space_or_negative_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': '200023', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_non_digit_is_invalid(self):
        self.assertFalse(validator.validate({'latitude': ' 200u23', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))


class ErrorValidatorLongitudeTestCase(TestCase):

    def test_null_no_pad_longitude_empty_string_dependencies_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '', 'latitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                 'coordinateMethodCode': ''}, {}, update=True))

    def test_null_no_pad_longitude_dependencies_missing_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ''}, {}, update=True))

    def test_null_pad_longitude_dependencies_missing_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' '}, {}, update=True))

    def test_null_pad_longitude_pad_dependencies_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' ', 'latitude': ' ',
                                                 'coordinateAccuracyCode': ' ', 'coordinateDatumCode': ' ',
                                                 'coordinateMethodCode': ' '}, {}, update=True))

    def test_positive_dms_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_double_digit_degrees_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' 0234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_single_digit_degrees_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' 0034556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' 0004556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' 0000556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' 0000056', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' 0000006', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' 0000000', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' 1805959', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(validator.validate({'longitude': ' 1234556.2', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            validator.validate({'longitude': ' 1234556.23', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            validator.validate({'longitude': ' 1234556.326', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '-1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_double_digit_degrees_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '-0234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_single_digit_degrees_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '-0034556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '-0004556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '-0000556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '-0000056', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '-0000006', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '-0000000', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '-1805959', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(validator.validate({'longitude': '-1234556.2', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            validator.validate({'longitude': '-1234556.23', 'latitude': ' 123456',
                                     'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                     'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            validator.validate({'longitude': '-1234556.326', 'latitude': ' 123456',
                                     'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                     'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_seconds_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 12345', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_minutes_seconds_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 123', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_degrees_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 1934556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_minutes_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 1238556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_seconds_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 1234576', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_too_many_seconds_decimals_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 1234556.2689', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('longitude')), 1)

    def test_dangling_decimal_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 1234556.', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('longitude')), 1)

    def test_too_long_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 12345566', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('longitude')), 1)

    def test_longer_than_maxlength_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 12345561232112', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('longitude')), 2)

    def test_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': '               ', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('longitude')), 1)
        self.assertIn('longitude', validator.errors.get('location')[0])

    def test_longitude_without_latitude_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 0400000',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('longitude', validator.errors.get('location')[0])

    def test_good_longitude_null_dependencies_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 0123456', 'latitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('longitude', validator.errors.get('location')[0])

    def test_good_longitude_non_exist_dependencies_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 0123456'}, {}, update=True))
        self.assertIn('longitude', validator.errors.get('location')[0])

    def test_good_longitude_good_latitude_null_dependencies_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('longitude', validator.errors.get('location')[0])

    def test_good_longitude_good_latitude_null_2_dependencies_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('longitude', validator.errors.get('location')[0])

    def test_good_longitude_good_latitude_null_1_dependency_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('longitude', validator.errors.get('location')[0])

    def test_first_char_not_space_or_negative_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': '1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_non_digit_is_invalid(self):
        self.assertFalse(validator.validate({'longitude': ' 123h556','latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))


class ErrorValidatorCoordinateAccuracyCodeTestCase(TestCase):

    def test_coordinate_accuracy_code_digit_in_ref_list_is_valid(self):
        self.assertTrue(validator.validate({'coordinateAccuracyCode': '1', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_coordinate_accuracy_code_char_in_ref_list_is_valid(self):
        self.assertTrue(validator.validate({'coordinateAccuracyCode': 'E', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_coordinate_accuracy_code_null_lat_long_null_is_valid(self):
        self.assertTrue(validator.validate({'coordinateAccuracyCode': '', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': '',
                                                 'coordinateMethodCode': ''}, {}, update=True))

    def test_coordinate_accuracy_code_longer_than_maxlength_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': 'E1', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('coordinateAccuracyCode')), 2)

    def test_coordinate_accuracy_code_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': '  ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        result = validator.errors.get('coordinateAccuracyCode')
        self.assertEqual(len(validator.errors.get('coordinateAccuracyCode')), 1)
        self.assertIn('coordinateAccuracyCode', validator.errors.get('location')[0])

    def test_coordinate_accuracy_code_lower_char_in_ref_list_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': 'e', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_coordinate_accuracy_code_null_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': ' ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', validator.errors.get('location')[0])

    def test_coordinate_accuracy_code_null_no_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', validator.errors.get('location')[0])

    def test_coordinate_accuracy_code_null_no_pad_lat_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': '', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', validator.errors.get('location')[0])

    def test_coordinate_accuracy_code_null_no_pad_lat_not_null_long_pad_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': '', 'longitude': ' ',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', validator.errors.get('location')[0])

    def test_coordinate_accuracy_code_null_no_pad_long_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': '', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', validator.errors.get('location')[0])

    def test_coordinate_accuracy_code_null_no_pad_long_not_null_lat_pad_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' ', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', validator.errors.get('location')[0])

    def test_coordinate_accuracy_code_not_null_lat_long_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': 'E', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', validator.errors.get('location')[0])

    def test_coordinate_accuracy_code_not_null_lat_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': 'E', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', validator.errors.get('location')[0])

    def test_coordinate_accuracy_code_not_null_long_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateAccuracyCode': 'E', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', validator.errors.get('location')[0])


class ErrorValidatorCoordinateMethodCodeTestCase(TestCase):

    def test_coordinate_method_code_char_in_ref_list_is_valid(self):
        self.assertTrue(validator.validate({'coordinateMethodCode': 'C', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_method_code_null_lat_long_null_is_valid(self):
        self.assertTrue(validator.validate({'coordinateMethodCode': '', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': '',
                                                 'coordinateAccuracyCode': ''}, {}, update=True))

    def test_coordinate_method_code_lower_char_in_ref_list_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': 'c', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_method_code_longer_than_maxlength_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': 'C3', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('coordinateMethodCode')), 2)

    def test_coordinate_method_code_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': '  ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('coordinateMethodCode')), 1)
        self.assertIn('coordinateMethodCode', validator.errors.get('location')[0])

    def test_coordinate_method_code_null_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': ' ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', validator.errors.get('location')[0])

    def test_coordinate_method_code_null_no_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', validator.errors.get('location')[0])

    def test_coordinate_method_code_null_no_pad_lat_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': '', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', validator.errors.get('location')[0])

    def test_coordinate_method_code_null_no_pad_lat_not_null_long_pad_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': '', 'longitude': ' ',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', validator.errors.get('location')[0])

    def test_coordinate_method_code_null_no_pad_long_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': '', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', validator.errors.get('location')[0])

    def test_coordinate_method_code_null_no_pad_long_not_null_lat_pad_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' ', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', validator.errors.get('location')[0])

    def test_coordinate_method_code_not_null_lat_long_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': 'C', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', validator.errors.get('location')[0])

    def test_coordinate_method_code_not_null_lat_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': 'C', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', validator.errors.get('location')[0])

    def test_coordinate_method_code_not_null_long_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateMethodCode': 'C', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', validator.errors.get('location')[0])


class ErrorValidatorCoordinateDatumCodeTestCase(TestCase):

    def test_coordinate_datum_code_char_in_ref_list_is_valid(self):
        self.assertTrue(validator.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                 'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_datum_code_lower_char_in_ref_list_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': 'barbados', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'c',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_datum_code_longer_than_maxlength_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': 'BARBADOS9103', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C3',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('coordinateDatumCode')), 2)

    def test_coordinate_datum_code_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': '             ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': '  ',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(validator.errors.get('coordinateDatumCode')), 1)
        self.assertIn('coordinateDatumCode', validator.errors.get('location')[0])

    def test_coordinate_datum_code_null_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': ' ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', validator.errors.get('location')[0])

    def test_coordinate_datum_code_null_no_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', validator.errors.get('location')[0])

    def test_coordinate_datum_code_null_no_pad_lat_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': '', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', validator.errors.get('location')[0])

    def test_coordinate_datum_code_null_no_pad_lat_not_null_long_pad_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': ' ',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', validator.errors.get('location')[0])

    def test_coordinate_datum_code_null_no_pad_long_not_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': '', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', validator.errors.get('location')[0])

    def test_coordinate_datum_code_null_no_pad_long_not_null_lat_pad_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' ', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', validator.errors.get('location')[0])

    def test_coordinate_datum_code_not_null_lat_long_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': '',
                                                 'latitude': '', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', validator.errors.get('location')[0])

    def test_coordinate_datum_code_not_null_lat_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', validator.errors.get('location')[0])

    def test_coordinate_datum_code_not_null_long_null_is_invalid(self):
        self.assertFalse(validator.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', validator.errors.get('location')[0])


class AltitudeErrorValidationsTestCase(TestCase):

    def test_optional(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': ' '}, {},)
        self.assertNotIn('altitude', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {})
        self.assertNotIn('altitude', validator.errors)

    def test_reciprocal_dependency(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345',  'altitudeAccuracyValue': 'a', 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitude', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeAccuracyValue': ' '},
            {'altitude': '12345',  'altitudeAccuracyValue': '1', 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertIn('altitude', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeMethodCode': ' '},
            {'altitude': '12345', 'altitudeAccuracyValue': '1', 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertIn('altitude', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeDatumCode': ' '},
            {'altitude': '12345', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertIn('altitude', validator.errors)


    def test_max_length(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1', 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitude', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '123456789', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', }, update=True)
        self.assertIn('altitude', validator.errors)

    def test_numeric(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertNotIn('altitude', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-12345'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertNotIn('altitude', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345.1'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertNotIn('altitude', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-12A'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertIn('altitude', validator.errors)

    def test_two_decimal_precison(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345.23'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertNotIn('altitude', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345.233'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertIn('altitude', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-1234.23'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertNotIn('altitude', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-1234.233'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertIn('altitude', validator.errors)


class AltitudeDatumCodeTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('altitudeDatumCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeDatumCode': '   '}, {}, update=False)
        self.assertNotIn('altitudeDatumCode', validator.errors)


    def test_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1' ,
             'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitudeDatumCode', validator.errors)

    def test_not_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1' ,
             'altitudeMethodCode': 'A', 'altitudeDatumCode': 'NAVD10'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('altitudeDatumCode', validator.errors)


class AltitudeMethodCodeTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('altitudeMethodCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeMethodCode': ' '}, {}, update=False)
        self.assertNotIn('altitudeMethodCode', validator.errors)


    def test_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1' ,
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitudeMethodCode', validator.errors)

    def test_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1' ,
             'altitudeMethodCode': 'B', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('altitudeMethodCode', validator.errors)


class AltitudeAccuracyValueTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('altitudeAccuracyValue', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeAccuracyValue': ' '}, {}, update=False)
        self.assertNotIn('altitudeAccuracyValue', validator.errors)

    def test_max_length(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '123' ,
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitudeAccuracyValue', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1234',
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('altitudeAccuracyValue', validator.errors)

    def test_numeric(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '.3',
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update = True)
        self.assertNotIn('altitudeAccuracyValue', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '-.3',
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitudeAccuracyValue', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': 'A.3',
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('altitudeAccuracyValue', validator.errors)


class NationalAquiferCodeTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('nationalAquiferCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': ' '}, {}, update=False)
        self.assertNotIn('nationalAquiferCode', validator.errors)

    def test_max_length(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'ABCDEFGHIJ'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('nationalAquiferCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'ABCDEFGHIJK'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('nationalAquiferCode', validator.errors)

    def test_aquifer_in_country_state(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100AKUNCD'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': 'US', 'stateFipsCode': '02'}, update=True)
        self.assertNotIn('nationalAquiferCode', validator.errors)

    def test_aquifer_not_in_country_state(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100ALLUVL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '02'}, update=True)
        self.assertIn('nationalAquiferCode', validator.errors)

    def test_aquifer_country_state_not_in_ref_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100AKUNCD'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'AZ', 'stateFipsCode': '02'}, update=True)
        self.assertIn('nationalAquiferCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100AKUNCD'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'RM', 'stateFipsCode': '02'}, update=True)
        self.assertIn('nationalAquiferCode', validator.errors)

    #TODO: Put back in when site type cross field json has been regenerated
    '''
    def test_invalid_non_null_code_site_type(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100AKUNCD'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'ST-CA'}, update=True)
        self.assertNotIn('siteTypeCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100AKUNCD'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-CI'}, update=True)
        self.assertIn('siteTypeCode', validator.errors)
    '''

class AquiferCodeTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('aquiferCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': ' '}, {}, update=False)
        self.assertNotIn('aquiferCode', validator.errors)

    def test_max_length(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '122CTHLS'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('aquiferCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '122CTHLSS'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('aquiferCode', validator.errors)

    def test_aquifer_in_country_state(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '400PCMB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '01'}, update=True)
        self.assertNotIn('aquiferCode', validator.errors)

    def test_aquifer_not_in_country_state(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '400PCMB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '02'}, update=True)
        self.assertIn('aquiferCode', validator.errors)

    def test_aquifer_for_country_state_not_in_ref_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '400PCMB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '80'}, update=True)
        self.assertIn('aquiferCode', validator.errors)

    #TODO: Put back in when site type cross field json is regenerate
    '''
    def test_invalid_non_null_code_for_site_type(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '400PCMB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '01', 'siteTypeCode': 'ST-CA'},
            update=True
        )
        self.assertNotIn('siteTypeCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '400PCMB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '01',
             'siteTypeCode': 'FA-CI'},
            update=True
        )
        self.assertIn('siteTypeCode', validator.errors)
    '''

class AquiferTypeCodeTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('aquiferTypeCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': ' '}, {}, update=False)
        self.assertNotIn('aquiferTypeCode', validator.errors)

    def test_max_length(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'U'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('aquiferTypeCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'UU'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('aquiferTypeCode', validator.errors)

    def test_aquifer_type_in_reference_list(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'U'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('aquiferTypeCode', validator.errors)

    def test_aquifer_type_not_in_reference_list(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'A'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('aquiferTypeCode', validator.errors)

    #TODO: Put back in when site type cross field json has been regenerated
    '''
    def test_invalid_non_null_code_for_site_type(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'U'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'ST-CA'}, update=True)
        self.assertNotIn('siteTypeCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'U'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-CI'}, update=True)
        self.assertIn('siteTypeCode', validator.errors)
    '''

class AgencyUseCodeTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('agencyUseCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'agencyUseCode': ' '}, {}, update=False)
        self.assertNotIn('agencyUseCode', validator.errors)

    def test_max_length(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'agencyUseCode': 'R'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('agencyUseCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'agencyUseCode': 'RR'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('agencyUseCode', validator.errors)

    def test_in_reference_list(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'agencyUseCode': 'R'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('agencyUseCode', validator.errors)

    def test_not_in_reference_list(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'agencyUseCode': 'U'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('agencyUseCode', validator.errors)


class DataReliabilityCodeTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('dataReliabilityCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': ' '}, {}, update=False)
        self.assertNotIn('dataReliabilityCode', validator.errors)

    def test_max_length(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': 'L'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('dataReliabilityCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': 'LL'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('dataReliabilityCode', validator.errors)

    def test_in_reference_list(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': 'L'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('dataReliabilityCode', validator.errors)

    def test_not_in_reference_list(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': 'A'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('dataReliabilityCode', validator.errors)


class DistrictCodeTestCase(TestCase):

    def test_required(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode' : '55'},
            {},
            update=False
        )
        self.assertNotIn('districtCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': ' '},
            {},
            update=False
        )
        self.assertIn('districtCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertIn('districtCode', validator.errors)

    def test_max_length(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': '122'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('districtCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': '1222'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
                           update=True
                           )
        self.assertIn('districtCode', validator.errors)

    def test_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': '55'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('districtCode', validator.errors)

    def test_not_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': '90'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('districtCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': '1'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('districtCode', validator.errors)


class CountryCodeTestCase(TestCase):

    def test_required(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode' : 'US'},
            {},
            update=False
        )
        self.assertNotIn('countryCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': ' '},
            {},
            update=False
        )
        self.assertIn('countryCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertIn('countryCode', validator.errors)

    def test_max_length(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('countryCode', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'USS'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
                           update=True
                           )
        self.assertIn('countryCode', validator.errors)

    def test_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('countryCode', validator.errors)

    def test_not_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'ZZ'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('countryCode', validator.errors)


class StateFipsCode(TestCase):

    def test_required(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode' : 'US'},
            {},
            update=False
        )
        self.assertNotIn('stateFipsCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': ' '},
            {},
            update=False
        )
        self.assertIn('stateFipsCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertIn('stateFipsCode', validator.errors)

    def test_max_length(self):
        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('stateFips', validator.errors)

        validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '055'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
                           update=True
                           )
        self.assertIn('stateFipsCode', validator.errors)

    def test_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US'},
            update=True
        )
        self.assertNotIn('stateFipsCode', validator.errors)

    def test_not_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '80'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US'},
            update=True
        )
        self.assertIn('stateFipsCode', validator.errors)

    def test_latitude_in_us_state_range(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'latitude': ' 430000'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55', 'countryCode': 'US'},
            update=True
        )
        self.assertNotIn('latitude', validator.errors)

    def test_latitude_not_in_us_state_range(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'latitude': ' 420000'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55', 'countryCode': 'US'},
            update=True
        )
        self.assertIn('latitude', validator.errors)

    def test_longitude_in_us_state_range(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'longitude': ' 0870000'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55', 'countryCode': 'US'},
            update=True
        )
        self.assertNotIn('longitude', validator.errors)

    def test_longitude_not_in_us_state_range(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'longitude': ' 0930000'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55', 'countryCode': 'US'},
            update=True
        )
        self.assertIn('longitude', validator.errors)


class CountyCodeTestCase(TestCase):

    def test_required(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'countyCode' : '003'},
            {},
            update=False
        )
        self.assertNotIn('countyCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'countyCode' : ''},
            {},
            update=False
        )
        self.assertIn('countyCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            {},
            update=False
        )
        self.assertIn('countyCode', validator.errors)

    def test_max_length(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countyCode' : '003'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'countyCode': '005'},
            update=True
        )
        self.assertNotIn('countyCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countyCode': '0003'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '005'},
            update=True
        )
        self.assertIn('countyCode', validator.errors)

    def test_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countyCode': '003'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'countyCode': '005'},
            update=True
        )
        self.assertNotIn('countyCode', validator.errors)

    def test_not_in_reference_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countyCode': '002'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '005'},
            update=True
        )
        self.assertIn('countyCode', validator.errors)


class MinorCivilDivisionCodeTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '005'},
            {},
            update=False
        )
        self.assertNotIn('minorCivilDivisionCode', validator.errors)

    def test_null_mcd_code(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'countyCode': '001'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': None}
        )
        self.assertNotIn('minorCivilDivisionCode', validator.errors)

    def test_ref_in_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': '00275'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '001'}
        )
        self.assertNotIn('minorCivilDivisionCode', validator.errors)

    def test_ref_not_in_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': '00277'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '001'}
        )
        self.assertIn('minorCivilDivisionCode', validator.errors)

    def test_country_state_county_not_in_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': '00277'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'CN', 'stateFipsCode': '55',
             'countyCode': '001'}
        )
        self.assertIn('minorCivilDivisionCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': '00277'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '85',
             'countyCode': '001'}
        )
        self.assertIn('minorCivilDivisionCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': '00277'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '002'}
        )
        self.assertIn('minorCivilDivisionCode', validator.errors)


class HydrologicUnitCodeTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            {},
            update=False
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'hydrologicUnitCode': '  '},
            {},
            update=False
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

    def test_valid_huc_in_ref_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode' : '07'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '0701'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '070102'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '07010206'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '0701020609'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '070102060903'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)


    def test_valid_huc_in_ref_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '07'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '0701'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '070102'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '07010206'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '0701020609'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '070102060903'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)

    def test_valid_huc_not_in_ref_list(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '08'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '0708'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '070103'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '07010207'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '0701020608'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '070102060904'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', validator.errors)

    def test_special_value(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '99999999'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', validator.errors)



class BasinCodeTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('basinCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'basinCode': '  '},
            {},
            update=False
        )
        self.assertNotIn('basinCode', validator.errors)

    def test_max_length(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'basinCode': 'AA'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('basinCode', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'basinCode': 'AAA'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('basinCode', validator.errors)


class MapNameTestCase(TestCase):
    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('mapName', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapName': '  '},
            {},
            update=False
        )
        self.assertNotIn('mapName', validator.errors)

    def test_max_length(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapName': '12345678901234567890'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('mapName', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapName': '123456789012345678901'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('mapName', validator.errors)


class MapScaleTestCase(TestCase):

    def test_optional(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('mapScale', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapScale': '  '},
            {},
            update=False
        )
        self.assertNotIn('mapScale', validator.errors)

    def test_max_length(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapScale': '1234567'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('mapScale', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapScale': '12345678'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('mapScale', validator.errors)

    def test_invalid_chars(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapScale': ' 123456'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('mapScale', validator.errors)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapScale': 'A123456'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('mapScale', validator.errors)




