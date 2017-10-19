
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
    #TODO: fill in with additional tests for latitude. Ideally each field that has validations would have a separate test case.

    def latitude_without_longitude_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 0400000'}, {}))

class ValidateCrossFieldsTestCase(TestCase):

    #TODO: Break this up so that a test case tests a fields validation rules. Below is the cross field validation schema tests
    #TODO: Add needed tests for all validations not just cross field.
    #TODO: Add tests with an existing document
    def setUp(self):
        self.validator = ErrorValidator()
        self.good_data = {
            'latitude': ' 123456',
            'longitude': ' 1234556',
            'coordinateAccuracyCode': '1',
            'coordinateDatumCode': 'ABIDJAN',
            'coordinateMethodCode': 'C'
        }
        self.good_data2 = {
            'altitude': '1234',
            'altitudeDatumCode': 'ASVD02',
            'altitudeMethodCode': 'A',
            'altitudeAccuracyValue': '12'
        }
        self.good_data3 = {
            'primaryUseOfSite': 'A',
            'secondaryUseOfSite': 'C',
            'tertiaryUseOfSiteCode': 'E'
        }
        self.good_data4 = {
            'primaryUseOfWaterCode': 'A',
            'secondaryUseOfWaterCode': 'C',
            'tertiaryUseOfWaterCode': 'E'
        }
        self.good_data5 = {
            'firstConstructionDate': '20000101',
            'siteEstablishmentDate': '20000102'
        }
        self.good_data6 = {
            'firstConstructionDate': '200001',
            'siteEstablishmentDate': '200101'
        }
        self.good_data7 = {
            'firstConstructionDate': '2000',
            'siteEstablishmentDate': '2001'
        }
        self.good_data8 = {
            'wellDepth': '10',
            'holeDepth': '10'
        }
        self.good_data9 = {
            'wellDepth': '10',
            'holeDepth': '11'
        }
        self.good_data10 = {
            'wellDepth': '',
            'holeDepth': '10'
        }
        self.good_data11 = {
            'wellDepth': '10',
            'holeDepth': ''
        }
        self.good_data12 = {
            'wellDepth': '',
            'holeDepth': ''
        }
        self.bad_data = {
            'latitude': '',
            'longitude': '',
            'coordinateAccuracyCode': '1',
            'coordinateDatumCode': 'ABIDJAN',
            'coordinateMethodCode': 'C'
        }
        self.bad_data2 = {
            'latitude': ' 123456',
            'longitude': '',
        }
        self.bad_data3 = {
            'latitude': '',
            'longitude': ' 1234556',
        }
        self.bad_data4 = {
            'latitude': ' 123456',
            'longitude': ' 1234556',
            'coordinateAccuracyCode': '',
            'coordinateDatumCode': 'ABIDJAN',
            'coordinateMethodCode': 'C'
        }
        self.bad_data5 = {
            'latitude': ' 123456',
            'longitude': ' 1234556',
            'coordinateAccuracyCode': '1',
            'coordinateDatumCode': '',
            'coordinateMethodCode': 'C'
        }
        self.bad_data6 = {
            'latitude': ' 123456',
            'longitude': ' 1234556',
            'coordinateAccuracyCode': '1',
            'coordinateDatumCode': 'ABIDJAN',
            'coordinateMethodCode': ''
        }
        self.bad_data7 = {
            'latitude': ' 123456',
            'longitude': ' 1234556',
            'coordinateAccuracyCode': '',
            'coordinateDatumCode': '',
            'coordinateMethodCode': ''
        }
        self.bad_data8 = {
            'altitude': '',
            'altitudeDatumCode': 'ASVD02',
            'altitudeAccuracyValue': '12',
            'altitudeMethodCode': 'A'
        }
        self.bad_data9 = {
            'altitude': '1234',
            'altitudeDatumCode': '',
            'altitudeAccuracyValue': '12',
            'altitudeMethodCode': 'A'
        }
        self.bad_data10 = {
            'altitude': '1234',
            'altitudeDatumCode': 'ASVD02',
            'altitudeAccuracyValue': '',
            'altitudeMethodCode': 'A'
        }
        self.bad_data11 = {
            'altitude': '1234',
            'altitudeDatumCode': 'ASVD02',
            'altitudeAccuracyValue': '12',
            'altitudeMethodCode': ''
        }
        self.bad_data12 = {
            'altitude': '1234',
            'altitudeDatumCode': '',
            'altitudeAccuracyValue': '',
            'altitudeMethodCode': ''
        }
        self.bad_data13 = {
            'primaryUseOfSite': 'A',
            'secondaryUseOfSite': 'A',
            'tertiaryUseOfSiteCode': 'A'
        }
        self.bad_data14 = {
            'primaryUseOfSite': 'A',
            'secondaryUseOfSite': 'A',
            'tertiaryUseOfSiteCode': 'C'
        }
        self.bad_data15 = {
            'primaryUseOfSite': 'A',
            'secondaryUseOfSite': 'C',
            'tertiaryUseOfSiteCode': 'A'
        }
        self.bad_data16 = {
            'primaryUseOfSite': 'C',
            'secondaryUseOfSite': 'A',
            'tertiaryUseOfSiteCode': 'A'
        }
        self.bad_data17 = {
            'primaryUseOfSite': '',
            'secondaryUseOfSite': 'C',
            'tertiaryUseOfSiteCode': 'E'
        }
        self.bad_data18 = {
            'primaryUseOfSite': 'A',
            'secondaryUseOfSite': '',
            'tertiaryUseOfSiteCode': 'E'
        }
        self.bad_data19 = {
            'primaryUseOfSite': '',
            'secondaryUseOfSite': '',
            'tertiaryUseOfSiteCode': 'E'
        }
        self.bad_data20 = {
            'primaryUseOfWaterCode': 'A',
            'secondaryUseOfWaterCode': 'A',
            'tertiaryUseOfWaterCode': 'A'
        }
        self.bad_data21 = {
            'primaryUseOfWaterCode': 'A',
            'secondaryUseOfWaterCode': 'A',
            'tertiaryUseOfWaterCode': 'C'
        }
        self.bad_data22 = {
            'primaryUseOfWaterCode': 'A',
            'secondaryUseOfWaterCode': 'C',
            'tertiaryUseOfWaterCode': 'A'
        }
        self.bad_data23 = {
            'primaryUseOfWaterCode': 'C',
            'secondaryUseOfWaterCode': 'A',
            'tertiaryUseOfWaterCode': 'A'
        }
        self.bad_data24 = {
            'primaryUseOfWaterCode': '',
            'secondaryUseOfWaterCode': 'C',
            'tertiaryUseOfWaterCode': 'E'
        }
        self.bad_data25 = {
            'primaryUseOfWaterCode': 'A',
            'secondaryUseOfWaterCode': '',
            'tertiaryUseOfWaterCode': 'E'
        }
        self.bad_data26 = {
            'primaryUseOfWaterCode': '',
            'secondaryUseOfWaterCode': '',
            'tertiaryUseOfWaterCode': 'E'
        }
        self.bad_data27 = {
            'firstConstructionDate': '20000102',
            'siteEstablishmentDate': '20000101'
        }
        self.bad_data28 = {
            'firstConstructionDate': '200002',
            'siteEstablishmentDate': '200001'
        }
        self.bad_data29 = {
            'firstConstructionDate': '2001',
            'siteEstablishmentDate': '2000'
        }
        self.bad_data30 = {
            'wellDepth': '11',
            'holeDepth': '10'
        }

    def test_validate_ok(self):
        self.assertTrue(self.validator.validate(self.good_data, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data2, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data3, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data4, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data5, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data6, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data7, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data8, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data9, {}, update=True))
        #TODO: Fix validate_type_numeric to return true for empty strings and strings with all blanks.
        #self.validator.validate(self.good_data10, {}, update=True)
        #self.assertTrue(self.validator.validate(self.good_data11, {}, update=True))
        #self.assertTrue(self.validator.validate(self.good_data12, {}, update=True))


    def test_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data2, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data3, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data4, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data5, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data6, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data7, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data8, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data9, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data10, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data11, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data12, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data13, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data14, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data15, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data16, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data17, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data18, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data19, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data20, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data21, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data22, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data23, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data24, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data25, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data26, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data27, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data28, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data29, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data30, {}, update=True))


