
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