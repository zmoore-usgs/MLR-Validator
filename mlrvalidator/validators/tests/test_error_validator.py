
from unittest import TestCase, mock

from ..error_validator import ErrorValidator


@mock.patch('mlrvalidator.validators.error_validator.SingleFieldValidator')
@mock.patch('mlrvalidator.validators.error_validator.CrossFieldErrorValidator')
@mock.patch('mlrvalidator.validators.error_validator.CrossFieldRefErrorValidator')
@mock.patch('mlrvalidator.validators.error_validator.TransitionValidator')
@mock.patch('mlrvalidator.validators.error_validator.open', mock.mock_open(read_data=''))
class ErrorValidatorErrorsTestCase(TestCase):

    def setUpPassingValidator(self, validator_class):
        """
        Given a mock validator class, tell its `validate` method to return `true`, and its `errors` property to be empty
        :param validator_class:
        :return:
        """
        validator = validator_class.return_value
        validator.validate.return_value = True
        validator.errors = {}

    def setUpPassingValidators(self, *validator_classes):
        """
        call self.setUpPassingValdator on all parameterized mock validator classes
        :param validator_classes:
        :return:
        """
        for validator_class in validator_classes:
            self.setUpPassingValidator(validator_class)

    def test_all_valid(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        self.setUpPassingValidators(mtran_class, mref_class, mcross_class, msingle_field_class)

        validator = ErrorValidator('schema_dir', 'ref_dir', 'http://localhost')
        result = validator.validate({'A' : 'This', 'B' : 'That'}, {})
        self.assertTrue(result)
        self.assertEqual(len(validator.errors), 0)

        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertTrue(result)
        self.assertEqual(len(validator.errors), 0)

    def test_single_field_invalid(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        self.setUpPassingValidators(mtran_class, mref_class, mcross_class)
        msingle_field = msingle_field_class.return_value
        msingle_field.validate.return_value = False
        msingle_field.errors = {'A' : ['Invalid']}

        validator = ErrorValidator('schema_dir', 'ref_dir', 'http://localhost')
        result = validator.validate({'A': 'This', 'B': 'That'}, {})
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('A', validator.errors)

        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('A', validator.errors)

    def test_cross_field_invalid(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        self.setUpPassingValidators(mtran_class, mref_class, msingle_field_class)
        mcross = mcross_class.return_value
        mcross.validate.return_value = False
        mcross.errors = {'B': ['Invalid']}

        validator = ErrorValidator('schema_dir', 'ref_dir', 'http://localhost')
        result = validator.validate({'A': 'This', 'B': 'That'}, {})
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('B', validator.errors)

        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('B', validator.errors)

    def test_ref_invalid(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        self.setUpPassingValidators(mtran_class, mcross_class, msingle_field_class)
        mref = mref_class.return_value
        mref.validate.return_value = False
        mref.errors = {'B': ['Bad']}

        validator = ErrorValidator('schema_dir', 'ref_dir', 'http://localhost')
        result = validator.validate({'A': 'This', 'B': 'That'}, {})
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('B', validator.errors)

        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('B', validator.errors)

    def test_tran_invalid(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        self.setUpPassingValidators(mref_class, mcross_class, msingle_field_class)
        mtran = mtran_class.return_value
        mtran.validate.return_value = False
        mtran.errors = {'B': ['Bad transition']}


        validator = ErrorValidator('schema_dir', 'ref_dir', 'http://localhost')
        result = validator.validate({'A': 'This', 'B': 'That'}, {})
        self.assertTrue(result)
        self.assertEqual(len(validator.errors), 0)

        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('B', validator.errors)

    def test_multiple_errors(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        mtran = mtran_class.return_value
        mref = mref_class.return_value
        mcross = mcross_class.return_value
        msingle_field = msingle_field_class.return_value

        mtran.validate.return_value = False
        mtran.errors = {'B': ['Bad transition']}
        mref.validate.return_value = False
        mref.errors = {'B': ['Bad ref']}
        mcross.validate.return_value = False
        mcross.errors = {'A': ['Invalid cross']}
        msingle_field.validate.return_value = False
        msingle_field.errors = {'B': ['Missing']}
        validator = ErrorValidator('schema_dir', 'ref_dir', 'http://localhost')
        result = validator.validate({'A': 'This', 'B': 'That'}, {})
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 2)
        self.assertEqual(len(validator.errors.get('A')), 1)
        self.assertEqual(len(validator.errors.get('B')), 2)

        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 2)
        self.assertEqual(len(validator.errors.get('A')), 1)
        self.assertEqual(len(validator.errors.get('B')), 3)

    def test_duplicate_site_error(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        self.setUpPassingValidators(mtran_class, mref_class, mcross_class, msingle_field_class)

        validator = ErrorValidator('schema_dir', 'ref_dir', 'http://localhost')
        self.assertFalse(validator.validate({'agencyCode': 'USGS', 'siteNumber': '12345678'}, {'agencyCode': 'USGS', 'siteNumber': '12345678'}))
        self.assertEqual(len(validator.errors), 1)
        self.assertTrue('duplicate_site' in validator.errors)








