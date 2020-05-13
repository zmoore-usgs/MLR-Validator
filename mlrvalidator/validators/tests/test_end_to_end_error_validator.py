
from unittest import TestCase

from app import application
from ..error_validator import ErrorValidator


class BaseE2ETestCase(TestCase):
    def setUp(self):
        self.v = ErrorValidator(application.config['SCHEMA_DIR'], application.config['LOCAL_REFERENCE_DIR'], application.config['REMOTE_REFERENCE_DIR'])


class ErrorValidatorAgencyCodeTestCase(BaseE2ETestCase):
    # We are leaving out the landNet validations for now as there too many questions as to how these will work
    # The existing land net validation is also well tested by unit tests.

    def test_agency_code_no_padding_is_valid(self):
        valid = self.v.validate({'agencyCode': 'USGS'}, {}, update=True)
        self.assertTrue(valid)

    def test_agency_code_padding_is_valid(self):
        self.assertTrue(self.v.validate({'agencyCode': 'USGS '}, {}, update=True))

    def test_agency_code_lower_padding_is_invalid(self):
        self.assertFalse(self.v.validate({'agencyCode': 'usgs   '}, {}, update=True))

    def test_agency_code_lower_no_padding_is_invalid(self):
        self.assertFalse(self.v.validate({'agencyCode': 'usgs'}, {}, update=True))

    def test_agency_code_not_in_ref_list_padding_is_invalid(self):
        self.assertFalse(self.v.validate({'agencyCode': 'XYZ   '}, {}, update=True))

    def test_agency_code_not_in_ref_list_no_padding_is_invalid(self):
        self.assertFalse(self.v.validate({'agencyCode': 'XYZ'}, {}, update=True))

    def test_agency_code_not_in_ref_list_padding_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'agencyCode': 'XYZ     '}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('agencyCode')), 2)

    def test_agency_code_in_ref_list_padding_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'agencyCode': 'USGS      '}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('agencyCode')), 1)

    def test_agency_code_null_is_invalid(self):
        self.assertFalse(self.v.validate({'agencyCode': ''}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('agencyCode')), 1)

    def test_agency_code_null_padding_is_invalid(self):
        self.assertFalse(self.v.validate({'agencyCode': ' '}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('agencyCode')), 1)

    def test_agency_code_padding_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'agencyCode': '           '}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('agencyCode')), 2)

    def test_agency_code_missing_on_insert_is_invalid(self):
        self.v.validate({'siteNumber': '9876543210'}, {}, update=False)
        self.assertIn('agencyCode', self.v.errors)


class ErrorValidatorSiteNumberTestCase(BaseE2ETestCase):

    def test_only_digits_is_valid(self):
        self.assertTrue(self.v.validate({'siteNumber': '01234567'}, {}, update=True))

    def test_only_digits_trailing_space_is_invalid(self):
        self.assertFalse(self.v.validate({'siteNumber': '01234   '}, {}, update=True))

    def test_null_value_no_pad_is_invalid(self):
        self.assertFalse(self.v.validate({'siteNumber': ''}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('siteNumber')), 2)

    def test_null_value_pad_is_invalid(self):
        self.assertFalse(self.v.validate({'siteNumber': ' '}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('siteNumber')), 2)

    def test_non_digit_is_invalid(self):
        self.assertFalse(self.v.validate({'siteNumber': 'a6'}, {}, update=True))

    def test_non_digit_special_char_is_invalid(self):
        self.assertFalse(self.v.validate({'siteNumber': '$'}, {}, update=True))

    def test_only_digits_blank_space_is_invalid(self):
        self.assertFalse(self.v.validate({'siteNumber': '32   4'}, {}, update=True))

    def test_only_digits_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'siteNumber': '0126954826512369548'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('siteNumber')), 1)

    def test_invalid_chars_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'siteNumber': '01269d82g651y23e69s548'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('siteNumber')), 2)

    def test_only_spaces_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'siteNumber': '                    '}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('siteNumber')), 3)

    def test_no_site_type_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': ' ', 'siteNumber': '12345678'}, {}, update=True))

    def test_no_site_number_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': 'AT', 'siteNumber': ' '}, {}, update=True))

    def test_only_digits_too_short_is_invalid(self):
        self.assertFalse(self.v.validate({'siteNumber': '0123'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('siteNumber')), 1)


class ErrorValidatorStationNameTestCase(BaseE2ETestCase):

    def test_valid_chars_all_lower_is_valid(self):
        self.assertTrue(self.v.validate({'stationName': 'br549'}, {}, update=True))

    def test_valid_chars_mix_upper_lower_is_valid(self):
        self.assertTrue(self.v.validate({'stationName': 'YYyyNnNN'}, {}, update=True))

    def test_valid_chars_all_upper_is_valid(self):
        self.assertTrue(self.v.validate({'stationName': 'ABCD'}, {}, update=True))

    def test_valid_chars_space_in_middle_is_valid(self):
        self.assertTrue(self.v.validate({'stationName': 'br 549'}, {}, update=True))

    def test_allowed_special_chars_is_valid(self):
        self.assertTrue(self.v.validate({'stationName': 'a-b'}, {}, update=True))

    def test_leading_space_is_valid(self):
        self.assertTrue(self.v.validate({'stationName': '   BR549'}, {}, update=True))

    def test_trailing_space_is_valid(self):
        self.assertTrue(self.v.validate({'stationName': 'BR549   '}, {}, update=True))

    def test_null_value_no_pad_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': ''}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('stationName')), 1)

    def test_null_value_pad_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': ' '}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('stationName')), 1)

    def test_bad_special_char_pound_sign_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': 'br5#49'}, {}, update=True))

    def test_bad_special_char_tab_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': 'br\t549'}, {}, update=True))

    def test_bad_special_char_backslash_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': 'br\\549'}, {}, update=True))

    def test_bad_special_char_dollar_sign_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': '$br549'}, {}, update=True))

    def test_bad_special_char_caret_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': 'b^r549'}, {}, update=True))

    def test_bad_special_char_asterisk_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': 'br5*49'}, {}, update=True))

    def test_bad_special_char_double_quotes_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': 'br54"9'}, {}, update=True))

    def test_bad_special_char_underscore_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': 'br549_'}, {}, update=True))

    def test_valid_chars_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': '0126954826512369548fesgdrs0126954826512369548fesgdrs'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('stationName')), 1)

    def test_invalid_chars_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': '01269d8#**2g65\\1y23e69s548                         '}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('stationName')), 2)

    def test_only_spaces_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'stationName': '                                                            '}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('stationName')), 2)

class ErrorValidatorLatitudeTestCase(BaseE2ETestCase):

    def test_null_no_pad_latitude_empty_string_dependencies_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': '', 'longitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                 'coordinateMethodCode': ''}, {}, update=True))

    def test_null_no_pad_latitude_dependencies_missing_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ''}, {}, update=True))

    def test_null_pad_latitude_dependencies_missing_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' '}, {}, update=True))

    def test_null_pad_latitude_pad_dependencies_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' ', 'longitude': ' ',
                                                 'coordinateAccuracyCode': ' ', 'coordinateDatumCode': ' ',
                                                 'coordinateMethodCode': ' '}, {}, update=True))

    def test_positive_dms_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_single_digit_degrees_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' 023456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' 003456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' 000456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' 000056', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' 000006', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' 000000', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' 905959', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': ' 900000.0', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            self.v.validate({'latitude': ' 900000.93', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            self.v.validate({'latitude': ' 900000.093', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': '-123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_single_digit_degrees_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': '-023456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': '-003456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': '-000456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': '-000056', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': '-000006', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': '-000000', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': '-905959', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'latitude': '-900000.0', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            self.v.validate({'latitude': '-900000.93', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            self.v.validate({'latitude': '-900000.093', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_seconds_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 9020', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_minutes_seconds_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 90', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_degrees_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 990000', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_minutes_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 207500', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_seconds_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 200066', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_too_many_seconds_decimals_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 200023.9234', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('latitude')), 1)

    def test_dangling_decimal_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 200023.', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('latitude')), 1)

    def test_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 20003234', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('latitude')), 1)

    def test_longer_than_maxlength_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 203300203234', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('latitude')), 2)

    def test_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': '             ', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('latitude')), 1)
        self.assertIn('latitude', self.v.errors.get('location')[0])

    def test_latitude_without_longitude_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 040000',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('latitude', self.v.errors.get('location')[0])

    def test_good_latitude_null_dependencies_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 123456', 'longitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('latitude', self.v.errors.get('location')[0])

    def test_good_latitude_non_exist_dependencies_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 123456'}, {}, update=True))
        self.assertIn('latitude', self.v.errors.get('location')[0])

    def test_good_latitude_good_longitude_null_dependencies_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('latitude', self.v.errors.get('location')[0])

    def test_good_latitude_good_longitude_null_2_dependencies_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('latitude', self.v.errors.get('location')[0])

    def test_good_latitude_good_longitude_null_1_dependency_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('latitude', self.v.errors.get('location')[0])

    def test_first_char_not_space_or_negative_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': '200023', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_non_digit_is_invalid(self):
        self.assertFalse(self.v.validate({'latitude': ' 200u23', 'longitude': ' 1234556',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_invalid_null_code_for_site_type(self):
        self.v.validate({'latitude': '', 'longitude': '',
                            'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                            'coordinateMethodCode': '', 'siteTypeCode': 'AT'}, {}, update=True)
        self.assertIn('latitude', self.v.errors['siteTypeCode'][0])

        self.v.validate({'latitude': '', 'longitude': '',
                            'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                            'coordinateMethodCode': '', 'siteTypeCode': 'AG'}, {}, update=True)
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                            'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                            'coordinateMethodCode': 'C', 'siteTypeCode': 'AS'}, {}, update=True)
        self.assertNotIn('siteTypeCode', self.v.errors)


class ErrorValidatorLongitudeTestCase(BaseE2ETestCase):

    def test_null_no_pad_longitude_empty_string_dependencies_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '', 'latitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                 'coordinateMethodCode': ''}, {}, update=True))

    def test_null_no_pad_longitude_dependencies_missing_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ''}, {}, update=True))

    def test_null_pad_longitude_dependencies_missing_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' '}, {}, update=True))

    def test_null_pad_longitude_pad_dependencies_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' ', 'latitude': ' ',
                                                 'coordinateAccuracyCode': ' ', 'coordinateDatumCode': ' ',
                                                 'coordinateMethodCode': ' '}, {}, update=True))

    def test_positive_dms_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_double_digit_degrees_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' 0234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_single_digit_degrees_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' 0034556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' 0004556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' 0000556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' 0000056', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' 0000006', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' 0000000', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' 1805959', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': ' 1234556.2', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            self.v.validate({'longitude': ' 1234556.23', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_positive_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            self.v.validate({'longitude': ' 1234556.326', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '-1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_double_digit_degrees_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '-0234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_single_digit_degrees_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '-0034556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_with_ms_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '-0004556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_single_digit_minutes_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '-0000556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_with_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '-0000056', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_single_digit_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '-0000006', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_zero_degrees_zero_minutes_zero_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '-0000000', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_max_degrees_max_minutes_max_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '-1805959', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_10ths_seconds_is_valid(self):
        self.assertTrue(self.v.validate({'longitude': '-1234556.2', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_100ths_seconds_is_valid(self):
        self.assertTrue(
            self.v.validate({'longitude': '-1234556.23', 'latitude': ' 123456',
                                     'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                     'coordinateMethodCode': 'C'}, {}, update=True))

    def test_negative_dms_with_1000ths_seconds_is_valid(self):
        self.assertTrue(
            self.v.validate({'longitude': '-1234556.326', 'latitude': ' 123456',
                                     'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                     'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_seconds_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 12345', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_missing_minutes_seconds_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 123', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_degrees_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 1934556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_minutes_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 1238556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_over_max_seconds_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 1234576', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_too_many_seconds_decimals_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 1234556.2689', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('longitude')), 1)

    def test_dangling_decimal_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 1234556.', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('longitude')), 1)

    def test_too_long_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 12345566', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('longitude')), 1)

    def test_longer_than_maxlength_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 12345561232112', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('longitude')), 2)

    def test_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': '               ', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('longitude')), 1)
        self.assertIn('longitude', self.v.errors.get('location')[0])

    def test_longitude_without_latitude_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 0400000',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('longitude', self.v.errors.get('location')[0])

    def test_good_longitude_null_dependencies_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 0123456', 'latitude': '',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('longitude', self.v.errors.get('location')[0])

    def test_good_longitude_non_exist_dependencies_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 0123456'}, {}, update=True))
        self.assertIn('longitude', self.v.errors.get('location')[0])

    def test_good_longitude_good_latitude_null_dependencies_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('longitude', self.v.errors.get('location')[0])

    def test_good_longitude_good_latitude_null_2_dependencies_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': '',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('longitude', self.v.errors.get('location')[0])

    def test_good_longitude_good_latitude_null_1_dependency_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': ''}, {}, update=True))
        self.assertIn('longitude', self.v.errors.get('location')[0])

    def test_first_char_not_space_or_negative_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': '1234556', 'latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_non_digit_is_invalid(self):
        self.assertFalse(self.v.validate({'longitude': ' 123h556','latitude': ' 123456',
                                                 'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_invalid_null_code_for_site_type(self):
        self.v.validate({'latitude': '', 'longitude': '',
                            'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                            'coordinateMethodCode': '', 'siteTypeCode': 'AT'}, {}, update=True)
        self.assertIn('longitude', self.v.errors['siteTypeCode'][0])

        self.v.validate({'latitude': '', 'longitude': '',
                            'coordinateAccuracyCode': '', 'coordinateDatumCode': '',
                            'coordinateMethodCode': '', 'siteTypeCode': 'AG'}, {}, update=True)
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate({'latitude': ' 123456', 'longitude': ' 1234556',
                            'coordinateAccuracyCode': '1', 'coordinateDatumCode': 'BARBADOS',
                            'coordinateMethodCode': 'C', 'siteTypeCode': 'AS'}, {}, update=True)
        self.assertNotIn('siteTypeCode', self.v.errors)


class ErrorValidatorCoordinateAccuracyCodeTestCase(BaseE2ETestCase):

    def test_coordinate_accuracy_code_digit_in_ref_list_is_valid(self):
        self.assertTrue(self.v.validate({'coordinateAccuracyCode': '1', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_coordinate_accuracy_code_char_in_ref_list_is_valid(self):
        self.assertTrue(self.v.validate({'coordinateAccuracyCode': 'E', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateMethodCode': 'C'}, {}, update=True))

    def test_coordinate_accuracy_code_null_lat_long_null_is_valid(self):
        self.assertTrue(self.v.validate({'coordinateAccuracyCode': '', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': '',
                                                 'coordinateMethodCode': ''}, {}, update=True))

    def test_coordinate_accuracy_code_longer_than_maxlength_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': 'E1', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('coordinateAccuracyCode')), 2)

    def test_coordinate_accuracy_code_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': '  ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        result = self.v.errors.get('coordinateAccuracyCode')
        self.assertEqual(len(self.v.errors.get('coordinateAccuracyCode')), 1)
        self.assertIn('coordinateAccuracyCode', self.v.errors.get('location')[0])

    def test_coordinate_accuracy_code_lower_char_in_ref_list_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': 'e', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))

    def test_coordinate_accuracy_code_null_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': ' ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', self.v.errors.get('location')[0])

    def test_coordinate_accuracy_code_null_no_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', self.v.errors.get('location')[0])

    def test_coordinate_accuracy_code_null_no_pad_lat_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': '', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', self.v.errors.get('location')[0])

    def test_coordinate_accuracy_code_null_no_pad_lat_not_null_long_pad_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': '', 'longitude': ' ',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', self.v.errors.get('location')[0])

    def test_coordinate_accuracy_code_null_no_pad_long_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': '', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', self.v.errors.get('location')[0])

    def test_coordinate_accuracy_code_null_no_pad_long_not_null_lat_pad_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' ', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', self.v.errors.get('location')[0])

    def test_coordinate_accuracy_code_not_null_lat_long_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': 'E', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', self.v.errors.get('location')[0])

    def test_coordinate_accuracy_code_not_null_lat_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': 'E', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', self.v.errors.get('location')[0])

    def test_coordinate_accuracy_code_not_null_long_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateAccuracyCode': 'E', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateMethodCode': 'C'}, {}, update=True))
        self.assertIn('coordinateAccuracyCode', self.v.errors.get('location')[0])


class ErrorValidatorCoordinateMethodCodeTestCase(BaseE2ETestCase):

    def test_coordinate_method_code_char_in_ref_list_is_valid(self):
        self.assertTrue(self.v.validate({'coordinateMethodCode': 'C', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                 'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_method_code_null_lat_long_null_is_valid(self):
        self.assertTrue(self.v.validate({'coordinateMethodCode': '', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': '',
                                                 'coordinateAccuracyCode': ''}, {}, update=True))

    def test_coordinate_method_code_lower_char_in_ref_list_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': 'c', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_method_code_longer_than_maxlength_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': 'C3', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('coordinateMethodCode')), 2)

    def test_coordinate_method_code_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': '  ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('coordinateMethodCode')), 1)
        self.assertIn('coordinateMethodCode', self.v.errors.get('location')[0])

    def test_coordinate_method_code_null_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': ' ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', self.v.errors.get('location')[0])

    def test_coordinate_method_code_null_no_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', self.v.errors.get('location')[0])

    def test_coordinate_method_code_null_no_pad_lat_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': '', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', self.v.errors.get('location')[0])

    def test_coordinate_method_code_null_no_pad_lat_not_null_long_pad_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': '', 'longitude': ' ',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', self.v.errors.get('location')[0])

    def test_coordinate_method_code_null_no_pad_long_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': '', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', self.v.errors.get('location')[0])

    def test_coordinate_method_code_null_no_pad_long_not_null_lat_pad_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' ', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', self.v.errors.get('location')[0])

    def test_coordinate_method_code_not_null_lat_long_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': 'C', 'longitude': '',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', self.v.errors.get('location')[0])

    def test_coordinate_method_code_not_null_lat_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': 'C', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', self.v.errors.get('location')[0])

    def test_coordinate_method_code_not_null_long_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateMethodCode': 'C', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateDatumCode': 'BARBADOS',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateMethodCode', self.v.errors.get('location')[0])


class ErrorValidatorCoordinateDatumCodeTestCase(BaseE2ETestCase):

    def test_coordinate_datum_code_char_in_ref_list_is_valid(self):
        self.assertTrue(self.v.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                 'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_datum_code_lower_char_in_ref_list_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': 'barbados', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'c',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))

    def test_coordinate_datum_code_longer_than_maxlength_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': 'BARBADOS9103', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C3',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('coordinateDatumCode')), 2)

    def test_coordinate_datum_code_longer_than_maxlength_spaces_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': '             ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': '  ',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertEqual(len(self.v.errors.get('coordinateDatumCode')), 1)
        self.assertIn('coordinateDatumCode', self.v.errors.get('location')[0])

    def test_coordinate_datum_code_null_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': ' ', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', self.v.errors.get('location')[0])

    def test_coordinate_datum_code_null_no_pad_lat_long_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', self.v.errors.get('location')[0])

    def test_coordinate_datum_code_null_no_pad_lat_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': '', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', self.v.errors.get('location')[0])

    def test_coordinate_datum_code_null_no_pad_lat_not_null_long_pad_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': ' ',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', self.v.errors.get('location')[0])

    def test_coordinate_datum_code_null_no_pad_long_not_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': '', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', self.v.errors.get('location')[0])

    def test_coordinate_datum_code_null_no_pad_long_not_null_lat_pad_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': '', 'longitude': ' 1234556',
                                                 'latitude': ' ', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', self.v.errors.get('location')[0])

    def test_coordinate_datum_code_not_null_lat_long_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': '',
                                                 'latitude': '', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', self.v.errors.get('location')[0])

    def test_coordinate_datum_code_not_null_lat_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': ' 1234556',
                                                 'latitude': '', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', self.v.errors.get('location')[0])

    def test_coordinate_datum_code_not_null_long_null_is_invalid(self):
        self.assertFalse(self.v.validate({'coordinateDatumCode': 'BARBADOS', 'longitude': '',
                                                 'latitude': ' 123456', 'coordinateMethodCode': 'C',
                                                  'coordinateAccuracyCode': 'E'}, {}, update=True))
        self.assertIn('coordinateDatumCode', self.v.errors.get('location')[0])


class AltitudeErrorValidationsTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': ' '}, {},)
        self.assertNotIn('altitude', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {})
        self.assertNotIn('altitude', self.v.errors)

    def test_reciprocal_dependency(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345',  'altitudeAccuracyValue': 'a', 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitude', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeAccuracyValue': ' '},
            {'altitude': '12345',  'altitudeAccuracyValue': '1', 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertIn('altitude', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeMethodCode': ' '},
            {'altitude': '12345', 'altitudeAccuracyValue': '1', 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertIn('altitude', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeDatumCode': ' '},
            {'altitude': '12345', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertIn('altitude', self.v.errors)


    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1', 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitude', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '123456789', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', }, update=True)
        self.assertIn('altitude', self.v.errors)

    def test_numeric(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertNotIn('altitude', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-12345'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertNotIn('altitude', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345.1'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertNotIn('altitude', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-12A'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertIn('altitude', self.v.errors)

    def test_two_decimal_precison(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345.23'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertNotIn('altitude', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345.233'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertIn('altitude', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-1234.23'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertNotIn('altitude', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-1234.233'},
            {'altitude': '1234', 'altitudeAccuracyValue': '1' , 'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertIn('altitude', self.v.errors)


class AltitudeDatumCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('altitudeDatumCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeDatumCode': '   '}, {}, update=False)
        self.assertNotIn('altitudeDatumCode', self.v.errors)


    def test_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1' ,
             'altitudeMethodCode': 'A', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitudeDatumCode', self.v.errors)

    def test_not_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1' ,
             'altitudeMethodCode': 'A', 'altitudeDatumCode': 'NAVD10'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('altitudeDatumCode', self.v.errors)


class AltitudeMethodCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('altitudeMethodCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeMethodCode': ' '}, {}, update=False)
        self.assertNotIn('altitudeMethodCode', self.v.errors)


    def test_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1' ,
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitudeMethodCode', self.v.errors)

    def test_not_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1' ,
             'altitudeMethodCode': 'B', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('altitudeMethodCode', self.v.errors)


class AltitudeAccuracyValueTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('altitudeAccuracyValue', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeAccuracyValue': ' '}, {}, update=False)
        self.assertNotIn('altitudeAccuracyValue', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '123' ,
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitudeAccuracyValue', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '1234',
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('altitudeAccuracyValue', self.v.errors)

    def test_numeric(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '.3',
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update = True)
        self.assertNotIn('altitudeAccuracyValue', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': '-.3',
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitudeAccuracyValue', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue': 'A.3',
             'altitudeMethodCode': 'D', 'altitudeDatumCode': 'BARGECANAL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('altitudeAccuracyValue', self.v.errors)


class NationalAquiferCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('nationalAquiferCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': ' '}, {}, update=False)
        self.assertNotIn('nationalAquiferCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'ABCDEFGHIJ'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('nationalAquiferCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'ABCDEFGHIJK'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('nationalAquiferCode', self.v.errors)

    def test_aquifer_in_country_state(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100AKUNCD'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': 'US', 'stateFipsCode': '02'}, update=True)
        self.assertNotIn('nationalAquiferCode', self.v.errors)

    def test_aquifer_not_in_country_state(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100ALLUVL'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '02'}, update=True)
        self.assertIn('nationalAquiferCode', self.v.errors)

    def test_aquifer_country_state_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100AKUNCD'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'AZ', 'stateFipsCode': '02'}, update=True)
        self.assertIn('nationalAquiferCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100AKUNCD'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'RM', 'stateFipsCode': '02'}, update=True)
        self.assertIn('nationalAquiferCode', self.v.errors)

    def test_invalid_non_null_code_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100AKUNCD'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'ST-CA'}, update=True)
        self.assertIn('nationalAquiferCode', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'ST-CA'}, update=True)
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalAquiferCode': 'N100AKUNCD'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-CI'}, update=True)
        self.assertNotIn('siteTypeCode', self.v.errors)


class AquiferCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('aquiferCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': ' '}, {}, update=False)
        self.assertNotIn('aquiferCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '122CTHLS'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('aquiferCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '122CTHLSS'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('aquiferCode', self.v.errors)

    def test_aquifer_in_country_state(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '400PCMB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '01'}, update=True)
        self.assertNotIn('aquiferCode', self.v.errors)

    def test_aquifer_not_in_country_state(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '400PCMB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '02'}, update=True)
        self.assertIn('aquiferCode', self.v.errors)

    def test_aquifer_for_country_state_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '400PCMB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '80'}, update=True)
        self.assertIn('aquiferCode', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '400PCMB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '01',
             'siteTypeCode': 'ST-CA'},
            update=True
        )
        self.assertIn('aquiferCode', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '01',
             'siteTypeCode': 'ST-CA'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferCode': '400PCMB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '01',
             'siteTypeCode': 'AG'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)


class AquiferTypeCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('aquiferTypeCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': ' '}, {}, update=False)
        self.assertNotIn('aquiferTypeCode', self.v.errors)

    def test_max_length(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'U'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('aquiferTypeCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'UU'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('aquiferTypeCode', self.v.errors)

    def test_aquifer_type_in_reference_list(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'U'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('aquiferTypeCode', self.v.errors)

    def test_aquifer_type_not_in_reference_list(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'A'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('aquiferTypeCode', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': ' '},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'ST-CA'}, update=True)
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'U'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'ST-CA'}, update=True)
        self.assertIn('aquiferTypeCode', self.v.errors['siteTypeCode'][0])

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'aquiferTypeCode': 'U'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AG'}, update=True)
        self.assertNotIn('siteTypeCode', self.v.errors)


class AgencyUseCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {}, update=False)
        self.assertNotIn('agencyUseCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'agencyUseCode': ' '}, {}, update=False)
        self.assertNotIn('agencyUseCode', self.v.errors)

    def test_max_length(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'agencyUseCode': 'R'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('agencyUseCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'agencyUseCode': 'RR'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('agencyUseCode', self.v.errors)

    def test_in_reference_list(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'agencyUseCode': 'R'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('agencyUseCode', self.v.errors)

    def test_not_in_reference_list(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'agencyUseCode': 'U'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('agencyUseCode', self.v.errors)


class DataReliabilityCodeTestCase(BaseE2ETestCase):

    def test_optional_for_site_type_code(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'SB-CV'}, {}, update=False)
        self.assertNotIn('dataReliabilityCode', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': ' ', 'siteTypeCode': 'SB-CV'},
            {}, update=False)
        self.assertNotIn('dataReliabilityCode', self.v.errors['siteTypeCode'][0])

    def test_not_optional_for_site_type_code(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'SP'}, {}, update=False)
        self.assertIn('dataReliabilityCode', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': ' ', 'siteTypeCode': 'SP'},
            {}, update=False)
        self.assertIn('dataReliabilityCode', self.v.errors['siteTypeCode'][0])

    def test_max_length(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': 'L'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('dataReliabilityCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': 'LL'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('dataReliabilityCode', self.v.errors)

    def test_in_reference_list(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': 'L'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('dataReliabilityCode', self.v.errors)

    def test_not_in_reference_list(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataReliabilityCode': 'A'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertIn('dataReliabilityCode', self.v.errors)


class DistrictCodeTestCase(BaseE2ETestCase):

    def test_required(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode' : '55'},
            {},
            update=False
        )
        self.assertNotIn('districtCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': ' '},
            {},
            update=False
        )
        self.assertIn('districtCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertIn('districtCode', self.v.errors)

    def test_max_length(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': '122'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('districtCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': '1222'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
                           update=True
                           )
        self.assertIn('districtCode', self.v.errors)

    def test_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': '55'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('districtCode', self.v.errors)

    def test_not_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': '90'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('districtCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'districtCode': '1'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('districtCode', self.v.errors)


class CountryCodeTestCase(BaseE2ETestCase):

    def test_required(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode' : 'US'},
            {},
            update=False
        )
        self.assertNotIn('countryCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': ' '},
            {},
            update=False
        )
        self.assertIn('countryCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertIn('countryCode', self.v.errors)

    def test_max_length(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('countryCode', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'USS'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
                           update=True
                           )
        self.assertIn('countryCode', self.v.errors)

    def test_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('countryCode', self.v.errors)

    def test_not_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'ZZ'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('countryCode', self.v.errors)


class StateFipsCode(BaseE2ETestCase):

    def test_required(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode' : 'US'},
            {},
            update=False
        )
        self.assertNotIn('stateFipsCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': ' '},
            {},
            update=False
        )
        self.assertIn('stateFipsCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertIn('stateFipsCode', self.v.errors)

    def test_max_length(self):
        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('stateFips', self.v.errors)

        self.v.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '055'},
                           {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
                           update=True
                           )
        self.assertIn('stateFipsCode', self.v.errors)

    def test_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US'},
            update=True
        )
        self.assertNotIn('stateFipsCode', self.v.errors)

    def test_not_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '80'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US'},
            update=True
        )
        self.assertIn('stateFipsCode', self.v.errors)

    def test_latitude_in_us_state_range(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'latitude': ' 430000'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55', 'countryCode': 'US'},
            update=True
        )
        self.assertNotIn('latitude', self.v.errors)

    def test_latitude_not_in_us_state_range(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'latitude': ' 420000'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55', 'countryCode': 'US'},
            update=True
        )
        self.assertIn('latitude', self.v.errors)

    def test_longitude_in_us_state_range(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'longitude': ' 0870000'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55', 'countryCode': 'US'},
            update=True
        )
        self.assertNotIn('longitude', self.v.errors)

    def test_longitude_not_in_us_state_range(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'longitude': ' 0930000'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'stateFipsCode': '55', 'countryCode': 'US'},
            update=True
        )
        self.assertIn('longitude', self.v.errors)


class CountyCodeTestCase(BaseE2ETestCase):

    def test_required(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'countyCode' : '003'},
            {},
            update=False
        )
        self.assertNotIn('countyCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'countyCode' : ''},
            {},
            update=False
        )
        self.assertIn('countyCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            {},
            update=False
        )
        self.assertIn('countyCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countyCode' : '003'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'countyCode': '005'},
            update=True
        )
        self.assertNotIn('countyCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countyCode': '0003'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '005'},
            update=True
        )
        self.assertIn('countyCode', self.v.errors)

    def test_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countyCode': '003'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'countyCode': '005'},
            update=True
        )
        self.assertNotIn('countyCode', self.v.errors)

    def test_not_in_reference_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countyCode': '002'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '005'},
            update=True
        )
        self.assertIn('countyCode', self.v.errors)


class MinorCivilDivisionCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '005'},
            {},
            update=False
        )
        self.assertNotIn('minorCivilDivisionCode', self.v.errors)

    def test_null_mcd_code(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'countyCode': '001'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': None},
            update=True
        )
        self.assertNotIn('minorCivilDivisionCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': None, 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '001'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('minorCivilDivisionCode', self.v.errors)

    def test_ref_in_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': '00275'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '001'},
            update=True
        )
        self.assertNotIn('minorCivilDivisionCode', self.v.errors)

    def test_ref_not_in_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': '00277'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '001'},
            update=True
        )
        self.assertIn('minorCivilDivisionCode', self.v.errors)

    def test_country_state_county_not_in_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': '00277'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'CN', 'stateFipsCode': '55',
             'countyCode': '001'},
            update=True
        )
        self.assertIn('minorCivilDivisionCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': '00277'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '85',
             'countyCode': '001'},
            update=True
        )
        self.assertIn('minorCivilDivisionCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'minorCivilDivisionCode': '00277'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '002'},
            update=True
        )
        self.assertIn('minorCivilDivisionCode', self.v.errors)


class HydrologicUnitCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            {},
            update=False
        )
        self.assertNotIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55', 'hydrologicUnitCode': '  '},
            {},
            update=False
        )
        self.assertNotIn('hydrologicUnitCode', self.v.errors)

    def test_valid_huc_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode' : '07'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '0701'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '27'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '070102'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '27'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '07010206'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '27'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '0701020609'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '27'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '070102060903'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '27'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', self.v.errors)

    def test_valid_huc_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '08'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '0708'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '070103'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '07010207'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '0701020608'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '070102060904'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertIn('hydrologicUnitCode', self.v.errors)

    def test_special_value(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'hydrologicUnitCode': '99999999'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55'},
            update=True
        )
        self.assertNotIn('hydrologicUnitCode', self.v.errors)


class BasinCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('basinCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'basinCode': '  '},
            {},
            update=False
        )
        self.assertNotIn('basinCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'basinCode': 'AA'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('basinCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'basinCode': 'AAA'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('basinCode', self.v.errors)


class MapNameTestCase(BaseE2ETestCase):
    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('mapName', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapName': '  '},
            {},
            update=False
        )
        self.assertNotIn('mapName', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapName': '12345678901234567890'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('mapName', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapName': '123456789012345678901'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('mapName', self.v.errors)


class MapScaleTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('mapScale', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapScale': '  '},
            {},
            update=False
        )
        self.assertNotIn('mapScale', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapScale': '1234567'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('mapScale', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapScale': '12345678'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('mapScale', self.v.errors)

    def test_invalid_chars(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapScale': ' 123456'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('mapScale', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'mapScale': 'A123456'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('mapScale', self.v.errors)


class NationalWaterUseCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('nationalWaterUseCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalWaterUse': ' '},
            {},
            update=False
        )
        self.assertNotIn('nationalWaterUseCode', self.v.errors)

    def test_valid_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalWaterUseCode': 'DO'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-CI'},
            update=True
        )
        self.assertNotIn('nationalWaterUseCode', self.v.errors)

    def test_invalid_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalWaterUseCode': 'DO'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-FON'},
            update=True
        )
        self.assertIn('nationalWaterUseCode', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalWaterUseCode': 'DO'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-QC'},
            update=True
        )
        self.assertIn('nationalWaterUseCode', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalWaterUseCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-QC'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'nationalWaterUseCode': 'DO'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AG'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)


class PrimaryUseOfSiteCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('primaryUseOfSiteCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': ' '},
            {},
            update=False
        )
        self.assertNotIn('primaryUseOfSiteCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=False
        )
        self.assertNotIn('primaryUseOfSiteCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'AA'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=False
        )
        self.assertIn('primaryUseOfSiteCode', self.v.errors)

    def test_in_reference(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('primaryUseOfSiteCode', self.v.errors)

    def test_not_in_reference(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'B'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('primaryUseOfSiteCode', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AW'},
            update=True
        )
        self.assertIn('primaryUseOfSiteCode', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AW'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AG'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

    def test_invalid_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'GW'},
            update=True
        )
        self.assertIn('primaryUseOfSiteCode', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'GW'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

    def test_create_gw_location_with_primary_use_of_site_code(self):
        self.v.validate(
            {
                "siteTypeCode": "GW",
                "primaryUseOfSiteCode": "U",
            },
            {}
        )
        site_type_code_error_message = self.v.errors['siteTypeCode'][0]

        self.assertNotIn('primaryUseOfSiteCode', site_type_code_error_message)
        self.assertNotIn('secondaryUseOfSiteCode', site_type_code_error_message)
        self.assertNotIn('tertiaryUseOfSiteCode', site_type_code_error_message)


class SecondaryUseOfSiteCode(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('secondaryUseOfSiteCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfSiteCode': ' '},
            {},
            update=False
        )
        self.assertNotIn('secondaryUseOfSiteCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfSiteCode': 'C'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A'},
            update=True
        )
        self.assertNotIn('secondaryUseOfSiteCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfSiteCode': 'CC'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A'},
            update=True
        )
        self.assertIn('secondaryUseOfSiteCode', self.v.errors)

    def test_in_reference(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfSiteCode': 'C'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A'},
            update=True
        )
        self.assertNotIn('secondaryUseOfSiteCode', self.v.errors)

    def test_not_in_reference(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfSiteCode': 'B'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A'},
            update=True
        )
        self.assertIn('secondaryUseOfSiteCode', self.v.errors)

    def test_secondary_without_primary(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfSiteCode': 'C'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('secondaryUseOfSiteCode', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfSiteCode': 'C'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AW'},
            update=True
        )
        self.assertIn('secondaryUseOfSiteCode', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfSiteCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AW'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfSiteCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AG'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)


class TertiaryUseOfSiteCode(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('tertiaryUseOfSiteCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfSiteCode': ' '},
            {},
            update=False
        )
        self.assertNotIn('tertiaryUseOfSiteCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfSiteCode': 'Z'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A', 'secondaryUseOfSiteCode': 'C'},
            update=True
        )
        self.assertNotIn('tertiaryUseOfSiteCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfSiteCode': 'ZZ'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A', 'secondaryUseOfSiteCode': 'C'},
            update=True
        )
        self.assertIn('tertiaryUseOfSiteCode', self.v.errors)

    def test_in_reference(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfSiteCode': 'Z'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A', 'secondaryUseOfSiteCode': 'C'},
            update=True
        )
        self.assertNotIn('tertiaryUseOfSiteCode', self.v.errors)

    def test_not_in_reference(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfSiteCode': 'B'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfSiteCode': 'A', 'secondaryUseOfSiteCode': 'C'},
            update=True
        )
        self.assertIn('tertiaryUseOfSiteCode', self.v.errors)

    def test_tertiary_without_secondary(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfSiteCode': 'B'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('tertiaryUseOfSiteCode', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfSiteCode': 'C'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AW'},
            update=True
        )
        self.assertIn('tertiaryUseOfSiteCode', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfSiteCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AW'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfSiteCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'AG'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

    def test_create_with_all_three_use_of_site_codes(self):
        self.v.validate(
            {
                "primaryUseOfSiteCode": "U",
                "secondaryUseOfSiteCode": "O",
                "tertiaryUseOfSiteCode": "H",
            },
            {}
        )
        self.assertNotIn('primaryUseOfSiteCode', self.v.errors)
        self.assertNotIn('secondaryUseOfSiteCode', self.v.errors)
        self.assertNotIn('tertiaryUseOfSiteCode', self.v.errors)


class PrimaryUseOfWaterCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('primaryUseOfWaterCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': ' '},
            {},
            update=False
        )
        self.assertNotIn('primaryUseOfWaterCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'A'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('primaryUseOfWaterCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'AA'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('primaryUseOfWaterCode', self.v.errors)

    def test_valid_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'A'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('primaryUseOfWaterCode', self.v.errors)

    def test_invalid_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'G'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('primaryUseOfWaterCode', self.v.errors)


class SecondaryUseOfWaterCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('secondaryUseOfWaterCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfWaterCode': ' '},
            {},
            update=False
        )
        self.assertNotIn('secondaryUseOfWaterCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfWaterCode': 'B'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'A'}
        )
        self.assertNotIn('secondaryUseOfWaterCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfWaterCode': 'BB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'A'}
        )
        self.assertIn('secondaryUseOfWaterCode', self.v.errors)

    def test_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfWaterCode': 'B'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'A'}
        )
        self.assertNotIn('secondaryUseOfWaterCode', self.v.errors)

    def test_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfWaterCode': 'G'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'A'}
        )
        self.assertIn('secondaryUseOfWaterCode', self.v.errors)

    def test_null_primary_with_secondary(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'secondaryUseOfWaterCode': 'B'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}
        )
        self.assertIn('secondaryUseOfWaterCode', self.v.errors)


class TertiaryUseOfWaterCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('tertiaryUseOfWaterCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfWaterCode': ' '},
            {},
            update=False
        )
        self.assertNotIn('tertiaryUseOfWaterCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfWaterCode': 'U'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'A', 'secondaryUseOfWaterCode': 'B'},
            update=True
        )
        self.assertNotIn('tertiaryUseOfWaterCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfWaterCode': 'UU'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'A', 'secondaryUseOfWaterCode': 'B'},
            update=True
        )
        self.assertIn('tertiaryUseOfWaterCode', self.v.errors)

    def test_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfWaterCode': 'U'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'A', 'secondaryUseOfWaterCode': 'B'},
            update=True
        )
        self.assertNotIn('tertiaryUseOfWaterCode', self.v.errors)

    def test_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfWaterCode': 'V'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'primaryUseOfWaterCode': 'A', 'secondaryUseOfWaterCode': 'B'},
            update=True
        )
        self.assertIn('tertiaryUseOfWaterCode', self.v.errors)

    def test_null_secondary_with_tertiary(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'tertiaryUseOfWaterCode': 'V'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('tertiaryUseOfWaterCode', self.v.errors)


class TopographicCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('topographicCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'topographicCode': ' '},
            {},
            update=False
        )
        self.assertNotIn('topographicCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'topographicCode': 'A'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('topographicCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'topographicCode': 'AA'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('topographicCode', self.v.errors)

    def test_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'topographicCode': 'A'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('topographicCode', self.v.errors)

    def test_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'topographicCode': 'Z'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('topographicCode', self.v.errors)


class InstrumentsCode(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('instrumentsCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'instrumentsCode': '   '},
            {},
            update=False
        )
        self.assertNotIn('instrumentsCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'instrumentsCode': 'YNYNYNYNYNYNYNYNYNYNYNYNYNYNYN'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('instrumentsCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'instrumentsCode': 'YNYNYNYNYNYNYNYNYNYNYNYNYNYNYNY'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('instrumentsCode', self.v.errors)

    def test_invalid_characters(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'instrumentsCode': '  YYYYNNN'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('instrumentsCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'instrumentsCode': '  YYYXNNN'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('instrumentsCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'instrumentsCode': '  YYY*NNN'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('instrumentsCode', self.v.errors)


class DataTypesCode(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('dataTypesCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataTypesCode': '   '},
            {},
            update=False
        )
        self.assertNotIn('dataTypesCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataTypesCode': 'AION AION AION AION AION AION '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('dataTypesCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataTypesCode': 'AION AION AION AION AION AION A'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('dataTypesCode', self.v.errors)

    def test_invalid_characters(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataTypesCode': '  AIONAOIN'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('dataTypesCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataTypesCode': '  AIOXAOIN'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('dataTypesCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'dataTypesCode': '  AION*AOIN'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('dataTypesCode', self.v.errors)


class ContributingDrainageAreaTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('contributingDrainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '   '},
            {},
            update=False
        )
        self.assertNotIn('contributingDrainageArea', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '12345678'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '99999999'},
            update= True
        )
        self.assertNotIn('contributingDrainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '123456789'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '99999999'},
            update=True
        )
        self.assertIn('contributingDrainageArea', self.v.errors)

    def test_positive_numeric(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '12345678'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '99999999'},
            update=True
        )
        self.assertNotIn('contributingDrainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '123.4567'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '99999999'},
            update=True
        )
        self.assertNotIn('contributingDrainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '-1234567'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '99999999'},
            update=True
        )
        self.assertIn('contributingDrainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '123A567'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '99999999'},
            update=True
        )
        self.assertIn('contributingDrainageArea', self.v.errors)

    def test_missing_drainage_area(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '123A567'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('contributingDrainageArea', self.v.errors)

    def test_cannot_be_larger_than_drainage_area(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '100'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '101'},
            update=True
        )
        self.assertNotIn('drainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '100'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '100'},
            update=True
        )
        self.assertNotIn('drainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '100'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '99'},
            update=True
        )
        self.assertIn('drainageArea', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '123.4567'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '99999999', 'siteTypeCode': 'FA-DV'},
            update=True
        )
        self.assertIn('contributingDrainageArea', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': ''},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '', 'siteTypeCode': 'FA-DV'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': ''},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '', 'siteTypeCode': 'ST'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)


class DrainageAreaTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('drainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '   '},
            {},
            update=False
        )
        self.assertNotIn('drainageArea', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '12345678'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('drainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '123456789'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('drainageArea', self.v.errors)

    def test_positive_numeric(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '12345678'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('drainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '-2345678'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('drainageArea', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '123A5678'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('drainageArea', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '99999999'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '99999999', 'siteTypeCode': 'FA-DV'},
            update=True
        )
        self.assertIn('drainageArea', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '',},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '', 'siteTypeCode': 'FA-DV'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': ''},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '', 'siteTypeCode': 'ST'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)


class FirstConstructionDateTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('firstConstructionDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '   '},
            {},
            update=False
        )
        self.assertNotIn('firstConstructionDate', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19921112'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('firstConstructionDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '199211121'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('firstConstructionDate', self.v.errors)

    def test_valid_date(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19921112'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('firstConstructionDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '1992111'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update = True
        )
        self.assertIn('firstConstructionDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19921330'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update = True
        )
        self.assertIn('firstConstructionDate', self.v.errors)

    def test_partial_dates(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '1992'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('firstConstructionDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '199210'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('firstConstructionDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '1992101'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('firstConstructionDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19921'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('firstConstructionDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '199'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('firstConstructionDate', self.v.errors)

    def test_construction_date_before_inventory_date(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19920315'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '19920320'},
            update=True
        )
        self.assertNotIn('site_dates', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '1992'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '19920320'},
            update=True
        )
        self.assertNotIn('site_dates', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19920315'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '1993'},
            update=True
        )
        self.assertNotIn('site_dates', self.v.errors)


    def test_construction_date_after_inventory_date(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19920315'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '19920220'},
            update=True
        )
        self.assertIn('site_dates', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '1993'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '19920320'},
            update=True
        )
        self.assertIn('site_dates', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19920315'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '1991'},
            update=True
        )
        self.assertIn('site_dates', self.v.errors)


class SiteEstablishmentDate(BaseE2ETestCase):
    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('siteEstablishmentDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '   '},
            {},
            update=False
        )
        self.assertNotIn('siteEstablishmentDate', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '19921112'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('siteEstablishmentDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '199211121'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('siteEstablishmentDate', self.v.errors)

    def test_valid_date(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '19921112'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('siteEstablishmentDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '1992111'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update = True
        )
        self.assertIn('siteEstablishmentDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '19921330'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update = True
        )
        self.assertIn('siteEstablishmentDate', self.v.errors)

    def test_partial_dates(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '1992'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('siteEstablishmentDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '199210'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('siteEstablishmentDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '1992101'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('siteEstablishmentDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '19921'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('siteEstablishmentDate', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '199'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('siteEstablishmentDate', self.v.errors)

    def test_construction_date_before_inventory_date(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '19920315'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19920215'},
            update=True
        )
        self.assertNotIn('site_dates', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '1993'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19920215'},
            update=True
        )
        self.assertNotIn('site_dates', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '199203'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19920215'},
            update=True
        )
        self.assertNotIn('site_dates', self.v.errors)

    def test_construction_date_after_inventory_date(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '19920215'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19920315'},
            update=True
        )
        self.assertIn('site_dates', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '199202'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19920315'},
            update=True
        )
        self.assertIn('site_dates', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteEstablishmentDate': '1992'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'firstConstructionDate': '19920315'},
            update=True
        )
        self.assertIn('site_dates', self.v.errors)


class HoleDepthTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('holeDepth', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'holeDepth': '   '},
            {},
            update=False
        )
        self.assertNotIn('holeDepth', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'holeDepth': ' 1234567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('holeDepth', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'holeDepth': ' 12345678'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('holeDepth', self.v.errors)

    def test_numeric(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'holeDepth': ' 1234567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('holeDepth', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'holeDepth': '-1234567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('holeDepth', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'holeDepth': ' 1234.67'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('holeDepth', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'holeDepth': ' 123A567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('holeDepth', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'holeDepth': '12345'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-QC'},
            update=True
        )
        self.assertIn('holeDepth', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'holeDepth': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-QC'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '9876543210', 'holeDepth': '12345'},
            {'agencyCode': 'USGS ', 'siteNumber': '9876543210', 'siteTypeCode': 'GW'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)


class WellDepthTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('wellDepth', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': '  '},
            {},
            update=False
        )
        self.assertNotIn('wellDepth', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': ' 1234567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('wellDepth', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': ' 12345678'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('wellDepth', self.v.errors)

    def test_numeric(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': ' 1234567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('wellDepth', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': '-1234567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('wellDepth', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': ' 1234.67'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('wellDepth', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': ' 123A567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('wellDepth', self.v.errors)

    def test_well_depth_greater_than_hole_depth(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': ' 123567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'holeDepth': ' 120000'},
            update=True
        )
        self.assertIn('depths', self.v.errors)

    def test_well_depth_less_than_hole_depth(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': ' 123567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'holeDepth': ' 130000'},
            update=True
        )
        self.assertNotIn('depths', self.v.errors)

    def test_depth_when_one_is_blank(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': ' 123567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'holeDepth': ' '},
            update=True
        )
        self.assertNotIn('depths', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'holeDepth': ' 123567'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'wellDepth': ' '},
            update=True
        )
        self.assertNotIn('depths', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'wellDepth': '12345'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-QC'},
            update=True
        )
        self.assertIn('wellDepth', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'wellDepth': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-QC'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '9876543210', 'wellDepth': '12345'},
            {'agencyCode': 'USGS ', 'siteNumber': '9876543210', 'siteTypeCode': 'GW'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)


class SourceOfDepthCodeTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('sourceOfDepthCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'sourceOfDepthCode': ' '},
            {},
            update=False
        )
        self.assertNotIn('sourceOfDepthCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'sourceOfDepthCode': 'A'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('sourceOfDepthCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'sourceOfDepthCode': 'AA'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('sourceOfDepthCode', self.v.errors)

    def test_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'sourceOfDepthCode': 'A'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('sourceOfDepthCode', self.v.errors)

    def test_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'sourceOfDepthCode': 'B'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('sourceOfDepthCode', self.v.errors)

    def test_invalid_non_null_code_for_site_type(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'sourceOfDepthCode': 'B'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-QC'},
            update=True
        )
        self.assertIn('sourceOfDepthCode', self.v.errors['siteTypeCode'][0])

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'sourceOfDepthCode': ' '},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteTypeCode': 'FA-QC'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '9876543210', 'sourceOfDepthCode': 'B'},
            {'agencyCode': 'USGS ', 'siteNumber': '9876543210', 'siteTypeCode': 'GW'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)


class ProjectNumberTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('projectNumber', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'projectNumber': '   '},
            {},
            update=False
        )
        self.assertNotIn('projectNumber', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'projectNumber': '123456789ABC'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('projectNumber', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'projectNumber': '123456789ABCD'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('projectNumber', self.v.errors)


class TimeZoneCodeTestCase(BaseE2ETestCase):

    def test_required(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertIn('timeZoneCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'timeZoneCode' : '  '},
            {},
            update=False
        )
        self.assertIn('timeZoneCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'timeZoneCode' : 'EST'},
            {},
            update=False
        )
        self.assertNotIn('timeZoneCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
         {'agencyCode': 'USGS', 'siteNumber': '12345678', 'timeZoneCode': 'ZP-11'},
         {'agencyCode': 'USGS', 'siteNumber': '12345678'},
         update=True
        )
        self.assertNotIn('timeZoneCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'timeZoneCode': 'ZZP-11'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('timeZoneCode', self.v.errors)

    def test_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'timeZoneCode': 'ZP-11'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('timeZoneCode', self.v.errors)

    def test_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'timeZoneCode': 'ZP-10'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('timeZoneCode', self.v.errors)


class DaylightSavingsTimeFlag(BaseE2ETestCase):

    def test_required(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertIn('daylightSavingsTimeFlag', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'daylightSavingsTimeFlag': '  '},
            {},
            update=False
        )
        self.assertIn('daylightSavingsTimeFlag', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'daylightSavingsTimeFlag': 'Y'},
            {},
            update=False
        )
        self.assertNotIn('daylightSavingsTimeFlag', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'daylightSavingsTimeFlag': 'Y'},
            {},
            update=False
        )
        self.assertNotIn('daylightSavingsTimeFlag', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'daylightSavingsTimeFlag': 'YY'},
            {},
            update=False
        )
        self.assertIn('daylightSavingsTimeFlag', self.v.errors)

    def test_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'daylightSavingsTimeFlag': 'Y'},
            {},
            update=False
        )
        self.assertNotIn('daylightSavingsTimeFlag', self.v.errors)

    def test_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'daylightSavingsTimeFlag': 'A'},
            {},
            update=False
        )
        self.assertIn('daylightSavingsTimeFlag', self.v.errors)


class SiteTypeCodeTestCase(BaseE2ETestCase):

    def test_required(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': '  '},
            {},
            update=False
        )
        self.assertIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '9876543210', 'siteTypeCode': 'FA-CS'},
            {},
            update=False
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

    def test_max_length(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '9876543210', 'siteTypeCode': 'FA-CS'},
            {'agencyCode': 'USGS', 'siteNumber': '9876543210', 'siteTypeCode': 'FA-CS'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '9876543210', 'siteTypeCode': 'FA-CIIII'},
            {'agencyCode': 'USGS', 'siteNumber': '9876543210', 'siteTypeCode': 'FA-CI'},
            update=True
        )
        self.assertIn('siteTypeCode', self.v.errors)

    def test_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'FA-CS'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'FA-CI'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

    def test_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'FA-CJ'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'FA-CI'},
            update=True
        )
        self.assertIn('siteTypeCode', self.v.errors)

    def test_for_allowed_transition(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'FA-CS'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'FA-PV'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)

    def test_for_invalid_transition(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'FA-CS'},
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'FA-OF'},
            update=True
        )
        self.assertIn('siteTypeCode', self.v.errors)

    def test_for_invalid_site_type_code_transition(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'AG'}, 
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'SS'},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)
        
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'ES', 'latitude': "12345678", 'longitude': "12345678"}, 
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'SS', 'latitude': "12345678", 'longitude': "12345678"},
            update=True
        )
        self.assertNotIn('siteTypeCode', self.v.errors)    

    def test_for_invalid_site_type_code(self):
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'SS'}, {},
            update=False
        )
        self.assertIn('siteTypeCode', self.v.errors)
        
        self.v.validate(
            {'agencyCode': 'USGS', 'siteNumber': '12345678', 'siteTypeCode': 'FA'}, {},
            update=False
        )
        self.assertIn('siteTypeCode', self.v.errors)

class RemarksTestCase(BaseE2ETestCase):

    def test_optional(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertNotIn('remarks', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'remarks': ''},
            {},
            update=False
        )
        self.assertNotIn('remarks', self.v.errors)

    def test_max_lenth(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'remarks': '12345678901234567890123456789012345678901234567890'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertNotIn('remarks', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678',
             'remarks': '123456789012345678901234567890123456789012345678901'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            update=True
        )
        self.assertIn('remarks', self.v.errors)


class SiteWebReadyCode(BaseE2ETestCase):

    def test_required(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'},
            {},
            update=False
        )
        self.assertIn('siteWebReadyCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteWebReadyCode': ' '},
            {},
            update=False
        )
        self.assertIn('siteWebReadyCode', self.v.errors)

        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteWebReadyCode': 'P'},
            {},
            update=False
        )
        self.assertNotIn('siteWebReadyCode', self.v.errors)

    def test_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteWebReadyCode': 'Y'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteWebReadyCode': 'P'},
            update=True
        )
        self.assertNotIn('siteWebReadyCode', self.v.errors)

    def test_not_in_ref_list(self):
        self.v.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteWebReadyCode': 'C'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'siteWebReadyCode': 'P'},
            update=True
        )
        self.assertIn('siteWebReadyCode', self.v.errors)
