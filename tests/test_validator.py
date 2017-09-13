
from unittest import TestCase
from schema import get_insert_schema

from validator import ValidateError, validate


class ValidateTestCase(TestCase):

    def setUp(self):
        self.data1 = {
            'agencyCode': 'USGS',
            'siteNumber': 'br549'
            }
        self.data2 = {
            'agencyCode': '',
            'siteNumber': 'br549'
            }
        self.schema = get_insert_schema()

    def test_validate_ok(self):
        self.assertTrue(validate(self.data1, self.schema))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.data2, self.schema)


class ValidateNumericCheck(TestCase):
    def setUp(self):
        self.good_data = {
            'altitude': '1234',
            }
        self.good_data2 = {
            'altitude': '12.34',
        }
        self.good_data3 = {
            'altitude': '0.1234',
        }
        self.good_data4 = {
            'altitude': '1234.',
        }
        self.good_data5 = {
            'altitude': '1234.0',
        }
        self.good_data6 = {
            'altitude': '1',
        }
        self.good_data7 = {
            'altitude': '-1234',
        }
        self.good_data8 = {
            'altitude': '-12.34',
        }
        self.good_data9 = {
            'altitude': '-0.1234',
        }
        self.good_data10 = {
            'altitude': '-1234.',
        }
        self.good_data11 = {
            'altitude': '-1234.0',
        }
        self.good_data12 = {
            'altitude': '-1',
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

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema))
        self.assertTrue(validate(self.good_data2, self.schema))
        self.assertTrue(validate(self.good_data3, self.schema))
        self.assertTrue(validate(self.good_data4, self.schema))
        self.assertTrue(validate(self.good_data5, self.schema))
        self.assertTrue(validate(self.good_data6, self.schema))
        self.assertTrue(validate(self.good_data7, self.schema))
        self.assertTrue(validate(self.good_data8, self.schema))
        self.assertTrue(validate(self.good_data9, self.schema))
        self.assertTrue(validate(self.good_data10, self.schema))
        self.assertTrue(validate(self.good_data11, self.schema))
        self.assertTrue(validate(self.good_data12, self.schema))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema)


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

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema))
        self.assertTrue(validate(self.good_data2, self.schema))
        self.assertTrue(validate(self.good_data3, self.schema))
        self.assertTrue(validate(self.good_data4, self.schema))
        self.assertTrue(validate(self.good_data5, self.schema))
        self.assertTrue(validate(self.good_data6, self.schema))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data6, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data7, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data8, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data9, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data10, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data11, self.schema)


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
            'instrumentsCode': 'K'
        }
        self.bad_data3 = {
            'instrumentsCode': 'N K'
        }
        self.bad_data4 = {
            'instrumentsCode': '9Y'
        }
        self.bad_data5 = {
            'instrumentsCode': '-Y'
        }
        self.bad_data6 = {
            'dataTypesCode': '-N'
        }
        self.bad_data7 = {
            'dataTypesCode': '3IOk'
        }
        self.bad_data8 = {
            'dataTypesCode': '/A'
        }
        self.schema = get_insert_schema()

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema))
        self.assertTrue(validate(self.good_data2, self.schema))
        self.assertTrue(validate(self.good_data3, self.schema))
        self.assertTrue(validate(self.good_data4, self.schema))
        self.assertTrue(validate(self.good_data5, self.schema))
        self.assertTrue(validate(self.good_data6, self.schema))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data6, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data7, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data8, self.schema)


class ValidateValidDMS(TestCase):

    def setUp(self):
        self.good_data = {
            'latitude': ' 123456',
        }
        self.good_data2 = {
            'latitude': '-123456',
        }
        self.good_data3 = {
            'latitude': ' 023456',
        }
        self.good_data4 = {
            'latitude': ' 003456',
        }
        self.good_data5 = {
            'latitude': ' 000456',
        }
        self.good_data6 = {
            'latitude': ' 000056',
        }
        self.good_data7 = {
            'latitude': ' 000006',
        }
        self.good_data8 = {
            'latitude': '-023456',
        }
        self.good_data9 = {
            'latitude': '-003456',
        }
        self.good_data10 = {
            'latitude': '-000456',
        }
        self.good_data11 = {
            'latitude': '-000056',
        }
        self.good_data12 = {
            'latitude': '-000006',
        }
        self.bad_data = {
            'latitude': 'k',
        }
        self.bad_data2 = {
            'latitude': 'fds342',
        }
        self.bad_data3 = {
            'latitude': '3',
        }
        self.bad_data4 = {
            'latitude': ' 127456',
        }
        self.bad_data5 = {
            'latitude': ' 123496',
        }
        self.bad_data6 = {
            'latitude': ' 923426',
        }
        self.bad_data7 = {
            'latitude': '-923426',
        }
        self.bad_data8 = {
            'latitude': '-127456',
        }
        self.bad_data9 = {
            'latitude': '-123496',
        }
        self.schema = get_insert_schema()

    def test_validate_ok(self):
        self.assertTrue(validate(self.good_data, self.schema))
        self.assertTrue(validate(self.good_data2, self.schema))
        self.assertTrue(validate(self.good_data3, self.schema))
        self.assertTrue(validate(self.good_data4, self.schema))
        self.assertTrue(validate(self.good_data5, self.schema))
        self.assertTrue(validate(self.good_data6, self.schema))
        self.assertTrue(validate(self.good_data7, self.schema))
        self.assertTrue(validate(self.good_data8, self.schema))
        self.assertTrue(validate(self.good_data9, self.schema))
        self.assertTrue(validate(self.good_data10, self.schema))
        self.assertTrue(validate(self.good_data11, self.schema))
        self.assertTrue(validate(self.good_data12, self.schema))

    def test_with_validate_not_ok(self):
        with self.assertRaises(ValidateError):
            validate(self.bad_data, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data2, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data3, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data4, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data5, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data6, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data7, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data8, self.schema)
        with self.assertRaises(ValidateError):
            validate(self.bad_data9, self.schema)
