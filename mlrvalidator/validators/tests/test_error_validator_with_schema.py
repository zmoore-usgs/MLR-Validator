
from unittest import TestCase

from ..error_validator import ErrorValidator


class ErrorValidatorAgencyCodeTestCase(TestCase):

    def setUp(self):
        self.validator = ErrorValidator()

    def test_agency_code_no_padding_is_valid(self):
        self.assertTrue(self.validator.validate({'agencyCode': 'USGS'}, {}, update=True))

    def test_agency_code_padding_is_valid(self):
        self.assertTrue(self.validator.validate({'agencyCode': 'USGS '}, {}, update=True))

    def test_agency_code_lower_padding_is_invalid(self):
        self.assertFalse(self.validator.validate({'agencyCode': 'usgs   '}, {}, update=True))

    def test_agency_code_lower_no_padding_is_invalid(self):
        self.assertFalse(self.validator.validate({'agencyCode': 'usgs'}, {}, update=True))

    def test_agency_code_not_in_ref_list_padding_is_invalid(self):
        self.assertFalse(self.validator.validate({'agencyCode': 'XYZ   '}, {}, update=True))

    def test_agency_code_not_in_ref_list_no_padding_is_invalid(self):
        self.assertFalse(self.validator.validate({'agencyCode': 'XYZ'}, {}, update=True))

    def test_agency_code_not_in_ref_list_padding_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'agencyCode': 'XYZ     '}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('agencyCode')), 2)

    def test_agency_code_in_ref_list_padding_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'agencyCode': 'USGS      '}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('agencyCode')), 1)

    def test_agency_code_not_in_ref_list_padding_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'agencyCode': 'USGS234    '}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('agencyCode')), 2)

    def test_agency_code_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'agencyCode': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('agencyCode')), 1)

    def test_agency_code_null_padding_is_invalid(self):
        self.assertFalse(self.validator.validate({'agencyCode': ' '}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('agencyCode')), 1)

    def test_agency_code_padding_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'agencyCode': '           '}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('agencyCode')), 2)


class ErrorValidatorSiteNumberTestCase(TestCase):

    def setUp(self):
        self.validator = ErrorValidator()

    def test_only_digits_is_valid(self):
        self.assertTrue(self.validator.validate({'siteNumber': '01234'}, {}, update=True))

    def test_only_digits_trailing_space_is_valid(self):
        self.assertTrue(self.validator.validate({'siteNumber': '01234   '}, {}, update=True))

    def test_null_value_no_pad_is_invalid(self):
        self.assertFalse(self.validator.validate({'siteNumber': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('siteNumber')), 1)

    def test_null_value_pad_is_invalid(self):
        self.assertFalse(self.validator.validate({'siteNumber': ' '}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('siteNumber')), 1)

    def test_non_digit_is_invalid(self):
        self.assertFalse(self.validator.validate({'siteNumber': 'a6'}, {}, update=True))

    def test_non_digit_special_char_is_invalid(self):
        self.assertFalse(self.validator.validate({'siteNumber': '$'}, {}, update=True))

    def test_only_digits_blank_space_is_invalid(self):
        self.assertFalse(self.validator.validate({'siteNumber': '32   4'}, {}, update=True))

    def test_only_digits_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'siteNumber': '0126954826512369548'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('siteNumber')), 1)

    def test_invalid_chars_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'siteNumber': '01269d82g651y23e69s548'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('siteNumber')), 2)

    def test_only_spaces_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'siteNumber': '                    '}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('siteNumber')), 2)


class ErrorValidatorStationNameTestCase(TestCase):

    def setUp(self):
        self.validator = ErrorValidator()

    def test_valid_chars_all_lower_is_valid(self):
        self.assertTrue(self.validator.validate({'stationName': 'br549'}, {}, update=True))

    def test_valid_chars_mix_upper_lower_is_valid(self):
        self.assertTrue(self.validator.validate({'stationName': 'YYyyNnNN'}, {}, update=True))

    def test_valid_chars_all_upper_is_valid(self):
        self.assertTrue(self.validator.validate({'stationName': 'ABCD'}, {}, update=True))

    def test_valid_chars_space_in_middle_is_valid(self):
        self.assertTrue(self.validator.validate({'stationName': 'br 549'}, {}, update=True))

    def test_allowed_special_chars_is_valid(self):
        self.assertTrue(self.validator.validate({'stationName': 'a-b'}, {}, update=True))

    def test_leading_space_is_valid(self):
        self.assertTrue(self.validator.validate({'stationName': '   BR549'}, {}, update=True))

    def test_trailing_space_is_valid(self):
        self.assertTrue(self.validator.validate({'stationName': 'BR549   '}, {}, update=True))

    def test_null_value_no_pad_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('stationName')), 1)

    def test_null_value_pad_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': ' '}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('stationName')), 1)

    def test_bad_special_char_pound_sign_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': 'br5#49'}, {}, update=True))

    def test_bad_special_char_tab_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': 'br\t549'}, {}, update=True))

    def test_bad_special_char_backslash_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': 'br\\549'}, {}, update=True))

    def test_bad_special_char_dollar_sign_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': '$br549'}, {}, update=True))

    def test_bad_special_char_caret_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': 'b^r549'}, {}, update=True))

    def test_bad_special_char_asterisk_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': 'br5*49'}, {}, update=True))

    def test_bad_special_char_double_quotes_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': 'br54"9'}, {}, update=True))

    def test_bad_special_char_underscore_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': 'br549_'}, {}, update=True))

    def test_valid_chars_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': '0126954826512369548fesgdrs0126954826512369548fesgdrs'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('stationName')), 1)

    def test_invalid_chars_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': '01269d8#**2g65\\1y23e69s548                         '}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('stationName')), 2)

    def test_only_spaces_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'stationName': '                                                            '}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('stationName')), 2)


class ErrorValidatorLatitudeTestCase(TestCase):

    def setUp(self):
        self.validator = ErrorValidator()

    def test_null_no_pad_latitude_empty_string_dependencies_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': '', 'longitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                 'coordinateMethodCode': ''}, {}, update=True))

    def test_null_no_pad_latitude_dependencies_missing_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ''}, {}, update=True))

    def test_null_pad_latitude_dependencies_missing_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' '}, {}, update=True))

    def test_null_pad_latitude_pad_dependencies_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' ', 'longitude': ' ',
                                                 'coordinateAccuracyCode': ' ', 'coordinateDatumCode': ' ',
                                                 'coordinateMethodCode': ' '}, {}, update=True))

    def test_positive_dms_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_single_digit_degrees_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' 023456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' 003456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' 000456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' 000056', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' 000006', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' 000000', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' 905959', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': ' 900000.0', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            self.validator.validate({'latitude': ' 900000.93', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            self.validator.validate({'latitude': ' 900000.093', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': '-123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_single_digit_degrees_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': '-023456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': '-003456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': '-000456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': '-000056', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': '-000006', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': '-000000', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': '-905959', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'latitude': '-900000.0', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            self.validator.validate({'latitude': '-900000.93', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            self.validator.validate({'latitude': '-900000.093', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_seconds_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 9020', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_minutes_seconds_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 90', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_degrees_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 990000', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_minutes_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 207500', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_seconds_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 200066', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_too_many_seconds_decimals_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 200023.9234', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 1)

    def test_dangling_decimal_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 200023.', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 1)

    def test_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 20003234', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 1)

    def test_longer_than_maxlength_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 203300203234', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 2)

    def test_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': '             ', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 5)

    def test_latitude_without_longitude_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 040000',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 1)

    def test_good_latitude_null_dependencies_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 123456', 'longitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 4)

    def test_good_latitude_non_exist_dependencies_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 123456'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 4)

    def test_good_latitude_good_longitude_null_dependencies_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 3)

    def test_good_latitude_good_longitude_null_2_dependencies_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 2)

    def test_good_latitude_good_longitude_null_1_dependency_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('latitude')), 1)

    def test_first_char_not_space_or_negative_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': '200023', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_non_digit_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 200u23', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))


class ErrorValidatorLongitudeTestCase(TestCase):

    def setUp(self):
        self.validator = ErrorValidator()

    def test_null_no_pad_longitude_empty_string_dependencies_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '', 'latitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                 'coordinateMethodCode': ''}, {}, update=True))

    def test_null_no_pad_longitude_dependencies_missing_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ''}, {}, update=True))

    def test_null_pad_longitude_dependencies_missing_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' '}, {}, update=True))

    def test_null_pad_longitude_pad_dependencies_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' ', 'latitude': ' ',
                                                 'coordinateAccuracyCode': ' ', 'coordinateDatumCode': ' ',
                                                 'coordinateMethodCode': ' '}, {}, update=True))

    def test_positive_dms_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_double_digit_degrees_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_single_digit_degrees_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0034556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0004556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0000556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0000056', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0000006', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0000000', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' 1805959', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': ' 1234556.2', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            self.validator.validate({'longitude': ' 1234556.23', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            self.validator.validate({'longitude': ' 1234556.326', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '-1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_double_digit_degrees_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '-0234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_single_digit_degrees_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '-0034556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '-0004556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '-0000556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '-0000056', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '-0000006', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '-0000000', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '-1805959', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(self.validator.validate({'longitude': '-1234556.2', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            self.validator.validate({'longitude': '-1234556.23', 'latitude': ' 123456',
                                     'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                     'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            self.validator.validate({'longitude': '-1234556.326', 'latitude': ' 123456',
                                     'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                     'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_seconds_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 12345', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_minutes_seconds_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 123', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_degrees_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 1934556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_minutes_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 1238556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_seconds_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 1234576', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_too_many_seconds_decimals_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 1234556.2689', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 1)

    def test_dangling_decimal_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 1234556.', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 1)

    def test_too_long_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 12345566', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 1)

    def test_longer_than_maxlength_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 12345561232112', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 2)

    def test_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': '               ', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 5)

    def test_longitude_without_latitude_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 0400000',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 1)

    def test_good_longitude_null_dependencies_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 0123456', 'latitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 4)

    def test_good_longitude_non_exist_dependencies_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 0123456'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 4)

    def test_good_longitude_good_latitude_null_dependencies_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 3)

    def test_good_longitude_good_latitude_null_2_dependencies_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 2)

    def test_good_longitude_good_latitude_null_1_dependency_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('longitude')), 1)

    def test_first_char_not_space_or_negative_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': '1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_non_digit_is_invalid(self):
        self.assertFalse(self.validator.validate({'longitude': ' 123h556','latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))


class ErrorValidatorCoordinateAccuracyCodeTestCase(TestCase):

    def setUp(self):
        self.validator = ErrorValidator()

    def test_coordinate_accuracy_code_digit_in_ref_list_is_valid(self):
        self.assertTrue(self.validator.validate({'coordinateAccuracyCode': '1', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_coordinate_accuracy_code_char_in_ref_list_is_valid(self):
        self.assertTrue(self.validator.validate({'coordinateAccuracyCode': 'E', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_coordinate_accuracy_code_null_lat_long_null_is_valid(self):
        self.assertTrue(self.validator.validate({'coordinateAccuracyCode': '', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': '',
                                                 'coordinateMethodCode': ''}, {}, update=True))

    def test_coordinate_accuracy_code_longer_than_maxlength_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': 'E1', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 2)

    def test_coordinate_accuracy_code_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': '  ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 3)

    def test_coordinate_accuracy_code_lower_char_in_ref_list_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': 'e', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_coordinate_accuracy_code_null_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': ' ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 2)

    def test_coordinate_accuracy_code_null_no_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 2)

    def test_coordinate_accuracy_code_null_no_pad_lat_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': '', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 1)

    def test_coordinate_accuracy_code_null_no_pad_lat_not_null_long_pad_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': '', 'longitude': ' ',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 1)

    def test_coordinate_accuracy_code_null_no_pad_long_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': '', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 1)

    def test_coordinate_accuracy_code_null_no_pad_long_not_null_lat_pad_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' ', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 1)

    def test_coordinate_accuracy_code_not_null_lat_long_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': 'E', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 2)

    def test_coordinate_accuracy_code_not_null_lat_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': 'E', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 1)

    def test_coordinate_accuracy_code_not_null_long_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateAccuracyCode': 'E', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateAccuracyCode')), 1)


class ErrorValidatorCoordinateMethodCodeTestCase(TestCase):

    def setUp(self):
        self.validator = ErrorValidator()

    def test_coordinate_method_code_char_in_ref_list_is_valid(self):
        self.assertTrue(self.validator.validate({'coordinateMethodCode': 'C', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_method_code_null_lat_long_null_is_valid(self):
        self.assertTrue(self.validator.validate({'coordinateMethodCode': '', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': '',
                                                 'coordinateAccuracyCode': ''}, {}, update=True))

    def test_coordinate_method_code_lower_char_in_ref_list_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': 'c', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_method_code_longer_than_maxlength_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': 'C3', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 2)

    def test_coordinate_method_code_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': '  ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 3)

    def test_coordinate_method_code_null_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': ' ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 2)

    def test_coordinate_method_code_null_no_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 2)

    def test_coordinate_method_code_null_no_pad_lat_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': '', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 1)

    def test_coordinate_method_code_null_no_pad_lat_not_null_long_pad_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': '', 'longitude': ' ',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 1)

    def test_coordinate_method_code_null_no_pad_long_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': '', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 1)

    def test_coordinate_method_code_null_no_pad_long_not_null_lat_pad_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' ', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 1)

    def test_coordinate_method_code_not_null_lat_long_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': 'C', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 2)

    def test_coordinate_method_code_not_null_lat_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': 'C', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 1)

    def test_coordinate_method_code_not_null_long_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateMethodCode': 'C', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateMethodCode')), 1)


class ErrorValidatorCoordinateDatumCodeTestCase(TestCase):

    def setUp(self):
        self.validator = ErrorValidator()

    def test_coordinate_datum_code_char_in_ref_list_is_valid(self):
        self.assertTrue(self.validator.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                 'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_datum_code_lower_char_in_ref_list_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': 'barbados', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'c',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_datum_code_longer_than_maxlength_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': 'BARBADOS9103', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C3',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 2)

    def test_coordinate_datum_code_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': '             ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': '  ',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 3)

    def test_coordinate_datum_code_null_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': ' ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 2)

    def test_coordinate_datum_code_null_no_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 2)

    def test_coordinate_datum_code_null_no_pad_lat_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': '', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 1)

    def test_coordinate_datum_code_null_no_pad_lat_not_null_long_pad_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': ' ',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 1)

    def test_coordinate_datum_code_null_no_pad_long_not_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': '', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 1)

    def test_coordinate_datum_code_null_no_pad_long_not_null_lat_pad_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' ', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 1)

    def test_coordinate_datum_code_not_null_lat_long_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': '',
                                                 'latitude': '', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 2)

    def test_coordinate_datum_code_not_null_lat_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 1)

    def test_coordinate_datum_code_not_null_long_null_is_invalid(self):
        self.assertFalse(self.validator.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('coordinateDatumCode')), 1)
