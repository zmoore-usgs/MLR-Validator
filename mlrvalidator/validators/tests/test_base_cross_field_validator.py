
from unittest import TestCase

from ..base_cross_field_validator import BaseCrossFieldValidator

class TestAnyFieldsInDocument(TestCase):

    def setUp(self):
        self.validator = BaseCrossFieldValidator()

    def test_any_fields(self):
        self.validator.validate({'field1': 'a', 'field2': 'b', 'field3': 'c'}, {})
        self.assertTrue(self.validator._any_fields_in_document(['field1', 'field3']))

        self.validator.validate({'field1': 'a'}, {})
        self.assertTrue(self.validator._any_fields_in_document(['field1', 'field3']))

        self.validator.validate({'field2': 'a', 'field3': 'c'}, {})
        self.assertTrue(self.validator._any_fields_in_document(['field1', 'field3']))

    def test_all_fields_missing_in_document(self):
        self.validator.validate({'field2': 'b'}, {'field1': 'a', 'field3': 'b'})
        self.assertFalse(self.validator._any_fields_in_document(['field1', 'field3']))
