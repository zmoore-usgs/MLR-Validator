
import json
import os
from unittest import TestCase, mock

from app import application

from ..reference import ReferenceInfo
from ..single_field_validator import SingleFieldValidator


class ValidateIsEmptyTestCase(TestCase):

    def setUp(self):
        self.validator = SingleFieldValidator(schema={'agencyCode': {'is_empty': False}}, reference_dir='')
        self.good_data = {
            'agencyCode': 'USGS'
        }
        self.bad_data = {
            'agencyCode': ''
        }
        self.bad_data2 = {
            'agencyCode': '   '
        }

    def test_validate_ok(self):
        self.assertTrue(self.validator.validate(self.good_data))

    def test_with_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data))
        self.assertFalse(self.validator.validate(self.bad_data2))


class ValidateValidSiteNumberTestCase(TestCase):

    def setUp(self):
        self.validator = SingleFieldValidator(schema={'siteNumber': {'valid_site_number': True}}, reference_dir='')
        self.only_digits_is_valid = {
            'siteNumber': '01234567'
        }
        self.null_value_no_pad_is_invalid = {
            'siteNumber': ''
        }
        self.null_value_pad_is_invalid = {
            'siteNumber': ' '
        }
        self.non_digit_is_invalid = {
            'siteNumber': 'a3'
        }
        self.non_digit_special_char_is_invalid = {
            'siteNumber': '$'
        }
        self.only_digits_blank_space_is_invalid = {
            'siteNumber': '32   4'
        }
        self.left_padding_is_invalid = {
            'siteNumber': '  12345'
        }

    def test_validate_ok(self):
        self.assertTrue(self.validator.validate(self.only_digits_is_valid))

    def test_with_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.non_digit_is_invalid))
        self.assertFalse(self.validator.validate(self.null_value_pad_is_invalid))
        self.assertFalse(self.validator.validate(self.null_value_no_pad_is_invalid))
        self.assertFalse(self.validator.validate(self.non_digit_special_char_is_invalid))
        self.assertFalse(self.validator.validate(self.only_digits_blank_space_is_invalid))
        self.assertFalse(self.validator.validate(self.left_padding_is_invalid))

class ValidateValidSiteTypeTestCase(TestCase):

    def setUp(self):
        ref_list = {'siteTypeInvalidCode': ['FA', 'SS']}
        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = SingleFieldValidator(schema={
                'siteTypeInvalidCode': {'valid_site_type': True}
            }, reference_dir='ref_dir')

        self.bad_data = {
            'siteTypeCode': 'FA'
        }
        self.bad_data2 = {
            'siteTypeCode': 'SS'
        }

    def test_with_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data))
        self.assertFalse(self.validator.validate(self.bad_data2))

class ValidateTypeNumericCheckTestCase(TestCase):

    def setUp(self):
        self.validator = SingleFieldValidator(schema={'altitude': {'type': 'numeric'}}, reference_dir='')
        self.good_data = {
            'altitude': '1234'
            }
        self.good_data2 = {
            'altitude': '12.34'
        }
        self.good_data3 = {
            'altitude': '0.12'
        }
        self.good_data4 = {
            'altitude': '1234.0'
        }
        self.good_data5 = {
            'altitude': '1'
        }
        self.good_data6 = {
            'altitude': '-1234'
        }
        self.good_data7 = {
            'altitude': '-12.34'
        }
        self.good_data8 = {
            'altitude': '-1234.0'
        }
        self.good_data9 = {
            'altitude': '-1'
        }
        self.good_data10 = {
            'altitude': ' '
        }
        self.bad_data = {
            'altitude': '-1df'
            }
        self.bad_data2 = {
            'altitude': 'f'
        }
        self.bad_data3 = {
            'altitude': '7-'
        }
        self.bad_data4 = {
            'altitude': '9.6.1'
        }
        self.bad_data5 = {
            'altitude': '9.p.1'
        }

    def test_validate_ok(self):
        self.assertTrue(self.validator.validate(self.good_data))
        self.assertTrue(self.validator.validate(self.good_data2))
        self.assertTrue(self.validator.validate(self.good_data3))
        self.assertTrue(self.validator.validate(self.good_data4))
        self.assertTrue(self.validator.validate(self.good_data5))
        self.assertTrue(self.validator.validate(self.good_data6))
        self.assertTrue(self.validator.validate(self.good_data7))
        self.assertTrue(self.validator.validate(self.good_data8))
        self.assertTrue(self.validator.validate(self.good_data9))
        self.assertTrue(self.validator.validate(self.good_data10))

    def test_with_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data))
        self.assertFalse(self.validator.validate(self.bad_data2))
        self.assertFalse(self.validator.validate(self.bad_data3))
        self.assertFalse(self.validator.validate(self.bad_data4))
        self.assertFalse(self.validator.validate(self.bad_data5))


class ValidateValidPrecisionTestCase(TestCase):

    def setUp(self):
        self.validator = SingleFieldValidator(schema={'altitude': {'valid_precision': True}}, reference_dir='')
        self.good_data = {
            'altitude': '1234'
            }
        self.good_data2 = {
            'altitude': '12.34'
        }
        self.good_data3 = {
            'altitude': '0.12'
        }
        self.good_data4 = {
            'altitude': '1234.0'
        }
        self.good_data5 = {
            'altitude': '1'
        }
        self.good_data6 = {
            'altitude': '-1234'
        }
        self.good_data7 = {
            'altitude': '-12.34'
        }
        self.good_data8 = {
            'altitude': '-1234.0'
        }
        self.good_data9 = {
            'altitude': '-1'
        }
        self.bad_data = {
            'altitude': '961.'
        }
        self.bad_data2 = {
            'altitude': '9.p.1'
        }
        self.bad_data3 = {
            'altitude': '9.242'
        }
        self.bad_data4 = {
            'altitude': '9.6.1'
        }
        self.bad_data5 = {
            'altitude': '234.f8'
        }

    def test_validate_ok(self):
        self.assertTrue(self.validator.validate(self.good_data))
        self.assertTrue(self.validator.validate(self.good_data2))
        self.assertTrue(self.validator.validate(self.good_data3))
        self.assertTrue(self.validator.validate(self.good_data4))
        self.assertTrue(self.validator.validate(self.good_data5))
        self.assertTrue(self.validator.validate(self.good_data6))
        self.assertTrue(self.validator.validate(self.good_data7))
        self.assertTrue(self.validator.validate(self.good_data8))
        self.assertTrue(self.validator.validate(self.good_data9))

    def test_with_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data))
        self.assertFalse(self.validator.validate(self.bad_data2))
        self.assertFalse(self.validator.validate(self.bad_data3))
        self.assertFalse(self.validator.validate(self.bad_data4))
        self.assertFalse(self.validator.validate(self.bad_data5))


class ValidateTypePositiveNumericTestCase(TestCase):
    def setUp(self):
        self.validator = SingleFieldValidator(schema={'contributingDrainageArea' : {'type': 'positive_numeric'}}, reference_dir='')
        self.good_data = {
            'contributingDrainageArea': '1234',
        }
        self.good_data2 = {
            'contributingDrainageArea': '12.34',
        }
        self.good_data3 = {
            'contributingDrainageArea': '0.1234',
        }
        self.good_data4 = {
            'contributingDrainageArea': '1234.',
        }
        self.good_data5 = {
            'contributingDrainageArea': '1234.0',
        }
        self.good_data6 = {
            'contributingDrainageArea': '1',
        }
        self.good_data7 = {
            'contributingDrainageArea': ' ',
        }
        self.bad_data = {
            'contributingDrainageArea': '-1234',
        }
        self.bad_data2 = {
            'contributingDrainageArea': '-12.34',
        }
        self.bad_data3 = {
            'contributingDrainageArea': '-0.1234',
        }
        self.bad_data4 = {
            'contributingDrainageArea': '-1234.',
        }
        self.bad_data5 = {
            'contributingDrainageArea': '-1234.0',
        }
        self.bad_data6 = {
            'contributingDrainageArea': '-1',
        }
        self.bad_data7 = {
            'contributingDrainageArea': '-1df'
        }
        self.bad_data8 = {
            'contributingDrainageArea': 'f'
        }
        self.bad_data9 = {
            'contributingDrainageArea': '7-'
        }
        self.bad_data10 = {
            'contributingDrainageArea': '9.6.1'
        }
        self.bad_data11 = {
            'contributingDrainageArea': '9.p.1'
        }

    def test_validate_ok(self):
        self.assertTrue(self.validator.validate(self.good_data))
        self.assertTrue(self.validator.validate(self.good_data2))
        self.assertTrue(self.validator.validate(self.good_data3))
        self.assertTrue(self.validator.validate(self.good_data4))
        self.assertTrue(self.validator.validate(self.good_data5))
        self.assertTrue(self.validator.validate(self.good_data6))
        self.assertTrue(self.validator.validate(self.good_data7))

    def test_with_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data))
        self.assertFalse(self.validator.validate(self.bad_data2))
        self.assertFalse(self.validator.validate(self.bad_data3))
        self.assertFalse(self.validator.validate(self.bad_data4))
        self.assertFalse(self.validator.validate(self.bad_data5))
        self.assertFalse(self.validator.validate(self.bad_data6))
        self.assertFalse(self.validator.validate(self.bad_data7))
        self.assertFalse(self.validator.validate(self.bad_data8))
        self.assertFalse(self.validator.validate(self.bad_data9))
        self.assertFalse(self.validator.validate(self.bad_data10))
        self.assertFalse(self.validator.validate(self.bad_data11))


class ValidateValidMapScaleCharsTestCase(TestCase):

    def setUp(self):
        self.validator = SingleFieldValidator(schema={'mapScale': {'valid_map_scale_chars': True}}, reference_dir='')
        self.good_data = {
            'mapScale': '24000'
        }
        self.good_data2 = {
            'mapScale': '24000  '
        }
        self.good_data3 = {
            'mapScale': '  24000'
        }
        self.bad_data = {
            'mapScale': '2.4000'
        }
        self.bad_data2 = {
            'mapScale': '24.000'
        }
        self.bad_data3 = {
            'mapScale': '24000.  '
        }
        self.bad_data4 = {
            'mapScale': '24,000'
        }

    def test_validate_ok(self):
        self.assertTrue(self.validator.validate(self.good_data))
        self.assertTrue(self.validator.validate(self.good_data2))
        self.assertTrue(self.validator.validate(self.good_data3))

    def test_with_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data))
        self.assertFalse(self.validator.validate(self.bad_data2))
        self.assertFalse(self.validator.validate(self.bad_data3))
        self.assertFalse(self.validator.validate(self.bad_data4))


class ValidateValidLatitudeDMS(TestCase):

    def setUp(self):
        self.validator = SingleFieldValidator(schema={'latitude': {'valid_latitude_dms': True}}, reference_dir='')
        self.good_data = {
            'latitude': ' 123456'
        }
        self.good_data2 = {
            'latitude': '-123456'
        }
        self.good_data3 = {
            'latitude': ' 023456'
        }
        self.good_data4 = {
            'latitude': ' 003456'
        }
        self.good_data5 = {
            'latitude': ' 000456'
        }
        self.good_data6 = {
            'latitude': ' 000056'
        }
        self.good_data7 = {
            'latitude': ' 000006'
        }
        self.good_data8 = {
            'latitude': '-023456'
        }
        self.good_data9 = {
            'latitude': '-003456'
        }
        self.good_data10 = {
            'latitude': '-000456'
        }
        self.good_data11 = {
            'latitude': '-000056'
        }
        self.good_data12 = {
            'latitude': '-000006'
        }
        self.good_data13 = {
            'latitude': '-000000'
        }
        self.good_data14 = {
            'latitude': ' 000000'
        }
        self.good_data15 = {
            'latitude': ' 905959'
        }
        self.good_data16 = {
            'latitude': ' 900000.0'
        }
        self.good_data17 = {
            'latitude': ' 900000.93'
        }
        self.good_data18 = {
            'latitude': ' 900000.093'
        }
        self.good_data20 = {
            'latitude': ' '
        }
        self.bad_data = {
            'latitude': 'k'
        }
        self.bad_data2 = {
            'latitude': 'fds342'
        }
        self.bad_data3 = {
            'latitude': '3'
        }
        self.bad_data4 = {
            'latitude': ' 127456'
        }
        self.bad_data5 = {
            'latitude': ' 123496'
        }
        self.bad_data6 = {
            'latitude': ' 923426'
        }
        self.bad_data7 = {
            'latitude': '-923426'
        }
        self.bad_data8 = {
            'latitude': '-127456'
        }
        self.bad_data9 = {
            'latitude': '-123496'
        }
        self.bad_data10 = {
            'latitude': '-126036'
        }
        self.bad_data11 = {
            'latitude': '-123060'
        }
        self.bad_data12 = {
            'latitude': ' 1.27456'
        }
        self.bad_data13 = {
            'latitude': ' 12.7456'
        }
        self.bad_data14 = {
            'latitude': ' 127.456'
        }
        self.bad_data15 = {
            'latitude': ' 1274.56'
        }
        self.bad_data16 = {
            'latitude': ' 12745.6'
        }
        self.bad_data17 = {
            'latitude': ' 900000.'
        }
        self.bad_data18 = {
            'latitude': ' 900000.-9'
        }
        self.bad_data19 = {
            'latitude': ' 1234564'
        }

    def test_validate_ok(self):
        self.assertTrue(self.validator.validate(self.good_data))
        self.assertTrue(self.validator.validate(self.good_data2))
        self.assertTrue(self.validator.validate(self.good_data3))
        self.assertTrue(self.validator.validate(self.good_data4))
        self.assertTrue(self.validator.validate(self.good_data5))
        self.assertTrue(self.validator.validate(self.good_data6))
        self.assertTrue(self.validator.validate(self.good_data7))
        self.assertTrue(self.validator.validate(self.good_data8))
        self.assertTrue(self.validator.validate(self.good_data9))
        self.assertTrue(self.validator.validate(self.good_data10))
        self.assertTrue(self.validator.validate(self.good_data11))
        self.assertTrue(self.validator.validate(self.good_data12))
        self.assertTrue(self.validator.validate(self.good_data13))
        self.assertTrue(self.validator.validate(self.good_data14))
        self.assertTrue(self.validator.validate(self.good_data15))
        self.assertTrue(self.validator.validate(self.good_data16))
        self.assertTrue(self.validator.validate(self.good_data17))
        self.assertTrue(self.validator.validate(self.good_data18))
        self.assertTrue(self.validator.validate(self.good_data20))

    def test_with_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data))
        self.assertFalse(self.validator.validate(self.bad_data2))
        self.assertFalse(self.validator.validate(self.bad_data3))
        self.assertFalse(self.validator.validate(self.bad_data4))
        self.assertFalse(self.validator.validate(self.bad_data5))
        self.assertFalse(self.validator.validate(self.bad_data6))
        self.assertFalse(self.validator.validate(self.bad_data7))
        self.assertFalse(self.validator.validate(self.bad_data8))
        self.assertFalse(self.validator.validate(self.bad_data9))
        self.assertFalse(self.validator.validate(self.bad_data10))
        self.assertFalse(self.validator.validate(self.bad_data11))
        self.assertFalse(self.validator.validate(self.bad_data12))
        self.assertFalse(self.validator.validate(self.bad_data13))
        self.assertFalse(self.validator.validate(self.bad_data14))
        self.assertFalse(self.validator.validate(self.bad_data15))
        self.assertFalse(self.validator.validate(self.bad_data16))
        self.assertFalse(self.validator.validate(self.bad_data17))
        self.assertFalse(self.validator.validate(self.bad_data18))
        self.assertFalse(self.validator.validate(self.bad_data19))


class ValidateValidLongitudeDMSTestCase(TestCase):

    def setUp(self):
        self.validator = SingleFieldValidator(schema={'longitude': {'valid_longitude_dms': True}}, reference_dir='')
        self.good_data = {
            'longitude': ' 1234556'
        }
        self.good_data2 = {
            'longitude': '-1234556'
        }
        self.good_data3 = {
            'longitude': ' 0234556'
        }
        self.good_data4 = {
            'longitude': ' 0034556'
        }
        self.good_data5 = {
            'longitude': ' 0004556'
        }
        self.good_data6 = {
            'longitude': ' 0000556'
        }
        self.good_data7 = {
            'longitude': ' 0000056'
        }
        self.good_data8 = {
            'longitude': '-0234556'
        }
        self.good_data9 = {
            'longitude': '-0034556'
        }
        self.good_data10 = {
            'longitude': '-0004556'
        }
        self.good_data11 = {
            'longitude': '-0000556'
        }
        self.good_data12 = {
            'longitude': '-0000006'
        }
        self.good_data13 = {
            'longitude': '-0000000'
        }
        self.good_data14 = {
            'longitude': '-1800000'
        }
        self.good_data15 = {
            'longitude': '-1800000.0'
        }
        self.good_data16 = {
            'longitude': '-1800000.01'
        }
        self.good_data17 = {
            'longitude': '-1800000.023'
        }
        self.good_data18 = {
            'longitude': ' 0880452.1  '
        }
        self.good_data19 = {
            'longitude': ' '
        }
        self.bad_data = {
            'longitude': 'k'
        }
        self.bad_data2 = {
            'longitude': 'fds342'
        }
        self.bad_data3 = {
            'longitude': '3'
        }
        self.bad_data4 = {
            'longitude': ' 1237456'
        }
        self.bad_data5 = {
            'longitude': ' 1233496'
        }
        self.bad_data6 = {
            'longitude': ' 1923426'
        }
        self.bad_data7 = {
            'longitude': '-1923426'
        }
        self.bad_data8 = {
            'longitude': '-1227456'
        }
        self.bad_data9 = {
            'longitude': '-1223496'
        }
        self.bad_data10 = {
            'longitude': ' 1.227456'
        }
        self.bad_data11 = {
            'longitude': ' 12.72456'
        }
        self.bad_data12 = {
            'longitude': ' 127.4546'
        }
        self.bad_data13 = {
            'longitude': ' 1274.546'
        }
        self.bad_data14 = {
            'longitude': ' 12745.64'
        }
        self.bad_data15 = {
            'longitude': ' 127246.4'
        }
        self.bad_data16 = {
            'longitude': '-1800000.'
        }
        self.bad_data17 = {
            'longitude': '-1800000.-02'
        }
        self.bad_data18 = {
            'longitude': '-1800000.-02'
        }
        self.bad_data19 = {
            'longitude': ' 123455622'
        }

    def test_validate_ok(self):
        self.assertTrue(self.validator.validate(self.good_data))
        self.assertTrue(self.validator.validate(self.good_data2))
        self.assertTrue(self.validator.validate(self.good_data3))
        self.assertTrue(self.validator.validate(self.good_data4))
        self.assertTrue(self.validator.validate(self.good_data5))
        self.assertTrue(self.validator.validate(self.good_data6))
        self.assertTrue(self.validator.validate(self.good_data7))
        self.assertTrue(self.validator.validate(self.good_data8))
        self.assertTrue(self.validator.validate(self.good_data9))
        self.assertTrue(self.validator.validate(self.good_data10))
        self.assertTrue(self.validator.validate(self.good_data11))
        self.assertTrue(self.validator.validate(self.good_data12))
        self.assertTrue(self.validator.validate(self.good_data13))
        self.assertTrue(self.validator.validate(self.good_data14))
        self.assertTrue(self.validator.validate(self.good_data15))
        self.assertTrue(self.validator.validate(self.good_data16))
        self.assertTrue(self.validator.validate(self.good_data17))
        self.assertTrue(self.validator.validate(self.good_data18))
        self.assertTrue(self.validator.validate(self.good_data19))

    def test_with_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data))
        self.assertFalse(self.validator.validate(self.bad_data2))
        self.assertFalse(self.validator.validate(self.bad_data3))
        self.assertFalse(self.validator.validate(self.bad_data4))
        self.assertFalse(self.validator.validate(self.bad_data5))
        self.assertFalse(self.validator.validate(self.bad_data6))
        self.assertFalse(self.validator.validate(self.bad_data7))
        self.assertFalse(self.validator.validate(self.bad_data8))
        self.assertFalse(self.validator.validate(self.bad_data9))
        self.assertFalse(self.validator.validate(self.bad_data10))
        self.assertFalse(self.validator.validate(self.bad_data11))
        self.assertFalse(self.validator.validate(self.bad_data12))
        self.assertFalse(self.validator.validate(self.bad_data13))
        self.assertFalse(self.validator.validate(self.bad_data14))
        self.assertFalse(self.validator.validate(self.bad_data15))
        self.assertFalse(self.validator.validate(self.bad_data16))
        self.assertFalse(self.validator.validate(self.bad_data17))
        self.assertFalse(self.validator.validate(self.bad_data18))
        self.assertFalse(self.validator.validate(self.bad_data19))


class ValidateValidDateTestCase(TestCase):

    def setUp(self):
        self.validator = SingleFieldValidator(schema={'firstConstructionDate': {'valid_date': True}}, reference_dir='')
        self.good_data = {
            'firstConstructionDate': '20140912'
        }
        self.good_data2 = {
            'firstConstructionDate': '201409  '
        }
        self.good_data3 = {
            'firstConstructionDate': '201409'
        }
        self.good_data4 = {
            'firstConstructionDate': '2014    '
        }
        self.good_data5 = {
            'firstConstructionDate': '2014'
        }
        self.good_data6 = {
            'firstConstructionDate': ' '
        }
        self.good_data7 = {
            'firstConstructionDate': ''
        }
        self.bad_data = {
            'firstConstructionDate': '20440912'
        }
        self.bad_data2 = {
            'firstConstructionDate': '2'
        }
        self.bad_data3 = {
            'firstConstructionDate': '2       '
        }
        self.bad_data4 = {
            'firstConstructionDate': '19'
        }
        self.bad_data5 = {
            'firstConstructionDate': '19      '
        }
        self.bad_data6 = {
            'firstConstructionDate': '198'
        }
        self.bad_data7 = {
            'firstConstructionDate': '198     '
        }
        self.bad_data8 = {
            'firstConstructionDate': '19821'
        }
        self.bad_data9 = {
            'firstConstructionDate': '19821   '
        }
        self.bad_data10 = {
            'firstConstructionDate': '1982122'
        }
        self.bad_data11 = {
            'firstConstructionDate': '1982122 '
        }
        self.bad_data12 = {
            'firstConstructionDate': '198212221'
        }
        self.bad_data13 = {
            'firstConstructionDate': '00001201'
        }
        self.bad_data14 = {
            'firstConstructionDate': '19821501'
        }
        self.bad_data15 = {
            'firstConstructionDate': '19821261'
        }
        self.bad_data16 = {
            'firstConstructionDate': '2014 912'
        }
        self.bad_data17 = {
            'firstConstructionDate': '201409 2'
        }
        self.bad_data18 = {
            'firstConstructionDate': '2014 9 2'
        }
        self.bad_data19 = {
            'firstConstructionDate': '2014O902'
        }

    def test_validate_ok(self):
        self.assertTrue(self.validator.validate(self.good_data))
        self.assertTrue(self.validator.validate(self.good_data2))
        self.assertTrue(self.validator.validate(self.good_data3))
        self.assertTrue(self.validator.validate(self.good_data4))
        self.assertTrue(self.validator.validate(self.good_data5))
        self.assertTrue(self.validator.validate(self.good_data6))
        self.assertTrue(self.validator.validate(self.good_data7))

    def test_with_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data))
        self.assertFalse(self.validator.validate(self.bad_data2))
        self.assertFalse(self.validator.validate(self.bad_data3))
        self.assertFalse(self.validator.validate(self.bad_data4))
        self.assertFalse(self.validator.validate(self.bad_data5))
        self.assertFalse(self.validator.validate(self.bad_data6))
        self.assertFalse(self.validator.validate(self.bad_data7))
        self.assertFalse(self.validator.validate(self.bad_data8))
        self.assertFalse(self.validator.validate(self.bad_data9))
        self.assertFalse(self.validator.validate(self.bad_data10))
        self.assertFalse(self.validator.validate(self.bad_data11))
        self.assertFalse(self.validator.validate(self.bad_data12))
        self.assertFalse(self.validator.validate(self.bad_data13))
        self.assertFalse(self.validator.validate(self.bad_data14))
        self.assertFalse(self.validator.validate(self.bad_data15))
        self.assertFalse(self.validator.validate(self.bad_data16))
        self.assertFalse(self.validator.validate(self.bad_data17))
        self.assertFalse(self.validator.validate(self.bad_data18))
        self.assertFalse(self.validator.validate(self.bad_data19))


class ValidateReferenceTestCase(TestCase):
    def setUp(self):
        ref_list = {'field1': ['A', 'B', 'C'], 'field2': ['AA', 'BB', 'CC']}
        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = SingleFieldValidator(schema={
                'field1': {'valid_reference': True},
                'field2': {'valid_reference': True}
            }, reference_dir='ref_dir')

    def test_valid_field(self):
        self.assertTrue(self.validator.validate({'field2': 'AA'}))

    def test_both_fields_good(self):
        self.assertTrue(self.validator.validate({'field1': 'A', 'field2': 'BB'}))

    def test_field_all_spaces(self):
        self.assertTrue(self.validator.validate({'field2': '   '}))

    def test_invalid_field(self):
        self.assertFalse(self.validator.validate({'field2': 'A'}))
    
    def test_right_padding_is_okay(self):
        self.assertTrue(self.validator.validate({'field1': 'A  '}))

class ValidateValidPaddingTestCase(TestCase):
    def setUp(self):
        ref_list = {'field1': ['A', 'B', 'C'], 'field2': ['AA', 'BB', 'CC']}
        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = SingleFieldValidator(schema={
                'field1': {'valid_padding': True},
                'field2': {'valid_padding': True}
            }, reference_dir='ref_dir')
    
    def test_field_preceding_left_spaces(self):
        self.assertFalse(self.validator.validate({'field1': '   A'}))
    
    def test_field_surrounded_by_spaces(self):
        self.assertFalse(self.validator.validate({'field1': '   A   '}))

    def test_site_number_padding(self):
        self.assertFalse(self.validator.validate({'siteNumber': '  12345678'}))
    
    def test_agency_code_padding(self):
        self.assertFalse(self.validator.validate({'agencyCode': '  USGS'}))

class ValidateSingleQuoteTestCase(TestCase):
    def setUp(self):
        self.validator = SingleFieldValidator(schema={'field1': {'valid_single_quotes': True}}, reference_dir='')

    def test_valid_field(self):
        self.assertTrue(self.validator.validate({'field1': '   '}))
        self.assertTrue(self.validator.validate({'field1': 'AAA'}))
        self.assertTrue(self.validator.validate({'field1': "A'A"}))

    def test_quote_at_end(self):
        self.assertFalse(self.validator.validate({'field1': "AAAA'"}))

    def test_quote_at_beginning(self):
        self.assertFalse(self.validator.validate({'field1': "'AAAA"}))


