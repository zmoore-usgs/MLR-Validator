from unittest import TestCase, mock

from ..warning_validator import WarningValidator

@mock.patch('mlrvalidator.validators.warning_validator.SingleFieldValidator')
@mock.patch('mlrvalidator.validators.warning_validator.CrossFieldRefWarningValidator')
class ErrorValidatorErrorsTestCase(TestCase):

    def test_all_valid(self, mcross_ref_class, msingle_field_class):
        msingle_field = msingle_field_class.return_value
        mcross_ref = mcross_ref_class.return_value

        msingle_field.validate.return_value = True
        msingle_field.errors = {}
        mcross_ref.validate.return_value = True
        mcross_ref.errors = {}

        validator = WarningValidator()

        self.assertTrue(validator.validate({'A' : 'This', 'B' : 'That'}, {}))
        self.assertEqual(len(validator.warnings), 0)

    def test_single_field_invalid(self, mcross_ref_class, msingle_field_class):
        mcross_ref = mcross_ref_class.return_value
        msingle_field = msingle_field_class.return_value

        msingle_field.validate.return_value = False
        msingle_field.errors = {'A' : ['Invalid']}
        mcross_ref.validate.return_value = True
        mcross_ref.errors = {}

        validator = WarningValidator()

        self.assertFalse(validator.validate({'A': 'This', 'B': 'That'}, {}))
        self.assertEqual(len(validator.warnings), 1)
        self.assertEqual(len(validator.warnings.get('A')), 1)

    def test_cross_field_ref_invalid(self, mcross_ref_class, msingle_field_class):
        mcross_ref = mcross_ref_class.return_value
        msingle_field = msingle_field_class.return_value

        msingle_field.validate.return_value = True
        msingle_field.errors = {}
        mcross_ref.validate.return_value = False
        mcross_ref.errors = {'A': ['Not good'], 'B': ['No match']}

        validator = WarningValidator()

        self.assertFalse(validator.validate({'A': 'This', 'B': 'That'}, {}))
        self.assertEqual(len(validator.warnings), 2)
        self.assertEqual(len(validator.warnings.get('A')), 1)
        self.assertEqual(len(validator.warnings.get('B')), 1)

    def test_multiple_invalid(self, mcross_ref_class, msingle_field_class):
        mcross_ref = mcross_ref_class.return_value
        msingle_field = msingle_field_class.return_value

        msingle_field.validate.return_value = False
        msingle_field.errors = {'A': ['Missing info']}
        mcross_ref.validate.return_value = False
        mcross_ref.errors = {'A': ['Not good'], 'B': ['No match']}

        validator = WarningValidator()

        self.assertFalse(validator.validate({'A': 'This', 'B': 'That'}, {}))
        self.assertEqual(len(validator.warnings), 2)
        self.assertEqual(len(validator.warnings.get('A')), 2)
        self.assertEqual(len(validator.warnings.get('B')), 1)
