
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


class TestValidateReciprocalDependency(TestCase):

    def setUp(self):
        self.validator = BaseCrossFieldValidator()

    def test_all_non_null(self):
        self.validator.validate({'field1': 'A', 'field3': 'B'}, {})
        self.validator._validate_reciprocal_dependency(['field1', 'field3'], 'required_fields')
        self.assertEqual(self.validator.errors, [])

        self.validator.validate({'field1': 'A'}, {'field3': 'B'})
        self.validator._validate_reciprocal_dependency(['field1', 'field3'], 'required_fields')
        self.assertEqual(self.validator.errors, [])

    def test_all_null(self):
        self.validator.validate({'field1': '   '}, {})
        self.validator._validate_reciprocal_dependency(['field1', 'field3'], 'required_fields')
        self.assertEqual(self.validator.errors, [])

        self.validator.validate({'field2': 'B'}, {'field3': '   '})
        self.validator._validate_reciprocal_dependency(['field1', 'field3'], 'required_fields')
        self.assertEqual(self.validator.errors, [])

    def test_some_null(self):
        self.validator.validate({'field1': 'A'}, {})
        self.validator._validate_reciprocal_dependency(['field1', 'field3'], 'required_fields')
        self.assertEqual(len(self.validator.errors), 1)
        self.assertTrue('required_fields' in self.validator.errors[0])

        self.validator.validate({'field1': '   ', 'field2': 'A'}, {'field3': 'C'})
        self.validator._validate_reciprocal_dependency(['field1', 'field3'], 'required_fields')
        self.assertEqual(len(self.validator.errors), 1)
        self.assertTrue('required_fields' in self.validator.errors[0])
