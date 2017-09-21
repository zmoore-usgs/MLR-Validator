
from unittest import TestCase
from schema import get_insert_schema, get_warning_schema
from site_file_validator_rules import SitefileValidator
from site_file_validator_warnings import SitefileWarningValidator
from validator import ValidateError, ValidateWarning, validate

class ValidateIsEmptyCase(TestCase):

    def setUp(self):
        self.good_data = {
            'agencyCode': 'USGS'
        }
        self.bad_data = {
            'agencyCode': ''
        }
        self.bad_data2 = {
            'agencyCode': '   '
        }
        self.schema = get_insert_schema()
        self.site_validator = SitefileValidator()
        self.site_validator.allow_unknown = True

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'error'))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema, self.site_validator, 'error')


class ValidateNumericCheck(TestCase):
    def setUp(self):
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
        self.schema = get_insert_schema()
        self.site_validator = SitefileValidator()
        self.site_validator.allow_unknown = True

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data2, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data3, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data4, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data5, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data6, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data7, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data8, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data9, self.schema, self.site_validator, 'error'))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema, self.site_validator, 'error')


class ValidateValidPrecisionCheck(TestCase):
    def setUp(self):
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
        self.bad_data4 = {
            'altitude': '234.f8'
        }
        self.schema = get_insert_schema()
        self.site_validator = SitefileValidator()
        self.site_validator.allow_unknown = True

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data2, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data3, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data4, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data5, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data6, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data7, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data8, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data9, self.schema, self.site_validator, 'error'))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema, self.site_validator, 'error')


class ValidatePositiveNumericCheck(TestCase):
    def setUp(self):
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
        self.schema = get_insert_schema()
        self.site_validator = SitefileValidator()
        self.site_validator.allow_unknown = True

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data2, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data3, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data4, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data5, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data6, self.schema, self.site_validator, 'error'))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data6, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data7, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data8, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data9, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data10, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data11, self.schema, self.site_validator, 'error')

class ValidateValidMapScaleCharsCase(TestCase):

    def setUp(self):
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
        self.schema = get_insert_schema()
        self.site_validator = SitefileValidator()
        self.site_validator.allow_unknown = True

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'error'))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema, self.site_validator, 'error')


class ValidateValidChars(TestCase):

    def setUp(self):
        self.good_data = {
            'stationName': 'br549'
            }
        self.good_data2 = {
            'instrumentsCode': 'YYYYNNNN'
        }
        self.good_data3 = {
            'instrumentsCode': 'NNNNYYYY'
        }
        self.good_data4 = {
            'instrumentsCode': 'NNNN YYYY'
        }
        self.good_data5 = {
            'instrumentsCode': ' '
        }
        self.good_data6 = {
            'instrumentsCode': 'yNyn '
        }
        self.good_data7 = {
            'dataTypesCode': 'NI OA'
        }
        self.good_data8 = {
            'dataTypesCode': ' OA'
        }
        self.good_data9 = {
            'dataTypesCode': 'o'
        }
        self.good_data10 = {
            'dataTypesCode': 'n '
        }
        self.bad_data = {
            'stationName': 'br5#49'
            }
        self.bad_data2 = {
            'stationName': 'br\t549'
        }
        self.bad_data3 = {
            'stationName': "br5\\49"
        }
        self.bad_data4 = {
            'stationName': '$br549'
        }
        self.bad_data5 = {
            'stationName': 'b^r549'
        }
        self.bad_data6 = {
            'stationName': 'br5*49'
        }
        self.bad_data7 = {
            'stationName': 'br54"9'
        }
        self.bad_data8 = {
            'stationName': 'br549_'
        }
        self.bad_data9 = {
            'instrumentsCode': 'K'
        }
        self.bad_data10 = {
            'instrumentsCode': 'N K'
        }
        self.bad_data11 = {
            'instrumentsCode': '9Y'
        }
        self.bad_data12 = {
            'instrumentsCode': '-Y'
        }
        self.bad_data13 = {
            'dataTypesCode': '-N'
        }
        self.bad_data14 = {
            'dataTypesCode': '3IOk'
        }
        self.bad_data15 = {
            'dataTypesCode': '/A'
        }
        self.schema = get_insert_schema()
        self.site_validator = SitefileValidator()
        self.site_validator.allow_unknown = True

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data2, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data3, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data4, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data5, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data6, self.schema, self.site_validator, 'error'))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data6, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data7, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data8, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data9, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data10, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data11, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data12, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data13, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data14, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data15, self.schema, self.site_validator, 'error')



class ValidateValidLatDMS(TestCase):

    def setUp(self):
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
            'latitude': ' 900000'
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
        self.good_data19 = {
            'latitude': ' 454856.27 '
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
            'latitude': ' 900000.5454'
        }

        self.schema = get_insert_schema()
        self.site_validator = SitefileValidator()
        self.site_validator.allow_unknown = True

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data2, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data3, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data4, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data5, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data6, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data7, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data8, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data9, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data10, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data11, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data12, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data13, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data14, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data15, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data16, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data17, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data18, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data19, self.schema, self.site_validator, 'error'))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data6, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data7, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data8, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data9, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data10, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data11, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data12, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data13, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data14, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data15, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data16, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data17, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data18, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data19, self.schema, self.site_validator, 'error')


class ValidateValidLongDMS(TestCase):

    def setUp(self):
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
            'longitude': '-1800000.0233'
        }
        self.bad_data18 = {
            'longitude': '-1800000.-02'
        }

        self.schema = get_insert_schema()
        self.site_validator = SitefileValidator()
        self.site_validator.allow_unknown = True

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data2, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data3, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data4, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data5, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data6, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data7, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data8, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data9, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data10, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data11, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data12, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data13, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data14, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data15, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data16, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data17, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data18, self.schema, self.site_validator, 'error'))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data6, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data7, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data8, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data9, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data10, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data11, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data12, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data13, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data14, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data15, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data16, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data17, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data18, self.schema, self.site_validator, 'error')

class ValidateValidDate(TestCase):

    def setUp(self):
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
        self.schema = get_insert_schema()
        self.site_validator = SitefileValidator()
        self.site_validator.allow_unknown = True

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data2, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data3, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data4, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data5, self.schema, self.site_validator, 'error'))


    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data6, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data7, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data8, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data9, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data10, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data11, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data12, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data13, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data14, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data15, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data16, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data17, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data18, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data19, self.schema, self.site_validator, 'error')


class ValidateLandNetCase(TestCase):

    def setUp(self):
        self.good_data = {
            'landNet': 'SWSWSWS010T09832R093425'
        }
        self.good_data2 = {
            'landNet': '      S15 T20N  R11E'
        }
        self.good_data3 = {
            'landNet': 'NWNWSWS15 T014N R022E 4'
        }
        self.good_data4 = {
            'landNet': '      S   T23N  R20E  4'
        }
        self.bad_data = {
            'landNet': 'Q'
        }
        self.bad_data2 = {
            'landNet': 'NWNWSWS15 T014N R02-E 4'
        }
        self.bad_data3 = {
            'landNet': 'NWNWSWS15  T014N R022E4'
        }
        self.bad_data4 = {
            'landNet': 'NWNWSW S15 T014N R022E4'
        }
        self.bad_data5 = {
            'landNet': 'NWNWSWS15 T014N R 022E 4'
        }
        self.bad_data6 = {
            'landNet': 'NWNWSWF15 T014N R 022E4'
        }
        self.bad_data7 = {
            'landNet': 'NWNWSWS15 S014N R 022E4'
        }
        self.bad_data8 = {
            'landNet': 'NWNWSWF15 T014N S 022E4'
        }
        self.schema = get_insert_schema()
        self.site_validator = SitefileValidator()
        self.site_validator.allow_unknown = True

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data2, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data3, self.schema, self.site_validator, 'error'))
        self.assertTrue(validate(self.good_data4, self.schema, self.site_validator, 'error'))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data6, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data7, self.schema, self.site_validator, 'error')
        with self.assertRaises(ValidateError):
            validate(self.bad_data8, self.schema, self.site_validator, 'error')


class ValidateWarningsCase(TestCase):

    def setUp(self):
        self.good_data = {
            'stationName': '12345'
        }
        self.bad_data = {
            'stationName': "12345'"
        }
        self.schema = get_warning_schema()
        self.site_validator = SitefileWarningValidator()
        self.site_validator.allow_unknown = True
        self.site_validator.name = 'warning'

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema, self.site_validator, 'warning'))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateWarning):
            validate(self.bad_data, self.schema, self.site_validator, 'warning')