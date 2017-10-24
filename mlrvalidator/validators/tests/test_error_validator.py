
from unittest import TestCase, mock

from ..error_validator import ErrorValidator

@mock.patch('mlrvalidator.validators.error_validator.SingleFieldValidator')
@mock.patch('mlrvalidator.validators.error_validator.CrossFieldErrorValidator')
@mock.patch('mlrvalidator.validators.error_validator.CrossFieldRefErrorValidator')
@mock.patch('mlrvalidator.validators.error_validator.TransitionValidator')
class ErrorValidatorErrorsTestCase(TestCase):

    def test_all_valid(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        mtran = mtran_class.return_value
        mref = mref_class.return_value
        mcross = mcross_class.return_value
        msingle_field = msingle_field_class.return_value

        mtran.validate.return_value = True
        mtran.errors = {}
        mref.validate.return_value = True
        mref.errors = {}
        mcross.validate.return_value = True
        mcross.errors = {}
        msingle_field.validate.return_value = True
        msingle_field.errors = {}

        validator = ErrorValidator()
        result = validator.validate({'A' : 'This', 'B' : 'That'}, {})
        self.assertTrue(result)
        self.assertEqual(len(validator.errors), 0)

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertTrue(result)
        self.assertEqual(len(validator.errors), 0)

    def test_single_field_invalid(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        mtran = mtran_class.return_value
        mref = mref_class.return_value
        mcross = mcross_class.return_value
        msingle_field = msingle_field_class.return_value

        mtran.validate.return_value = True
        mtran.errors = {}
        mref.validate.return_value = True
        mref.errors = {}
        mcross.validate.return_value = True
        mcross.errors = {}
        msingle_field.validate.return_value = False
        msingle_field.errors = {'A' : ['Invalid']}

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {})
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('A', validator.errors)

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('A', validator.errors)

    def test_cross_field_invalid(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        mtran = mtran_class.return_value
        mref = mref_class.return_value
        mcross = mcross_class.return_value
        msingle_field = msingle_field_class.return_value

        mtran.validate.return_value = True
        mtran.errors = {}
        mref.validate.return_value = True
        mref.errors = {}
        mcross.validate.return_value = False
        mcross.errors = {'B': ['Invalid']}
        msingle_field.validate.return_value = True
        msingle_field.errors = {}

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {})
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('B', validator.errors)

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('B', validator.errors)

    def test_ref_invalid(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        mtran = mtran_class.return_value
        mref = mref_class.return_value
        mcross = mcross_class.return_value
        msingle_field = msingle_field_class.return_value

        mtran.validate.return_value = True
        mtran.errors = {}
        mref.validate.return_value = False
        mref.errors = {'B': ['Bad']}
        mcross.validate.return_value = True
        mcross.errors = {}
        msingle_field.validate.return_value = True
        msingle_field.errors = {}

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {})
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('B', validator.errors)

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)
        self.assertIn('B', validator.errors)

    def test_tran_invalid(self, mtran_class, mref_class, mcross_class, msingle_field_class):
        mtran = mtran_class.return_value
        mref = mref_class.return_value
        mcross = mcross_class.return_value
        msingle_field = msingle_field_class.return_value

        mtran.validate.return_value = False
        mtran.errors = {'B': ['Bad transition']}
        mref.validate.return_value = True
        mref.errors = {}
        mcross.validate.return_value = True
        mcross.errors = {}
        msingle_field.validate.return_value = True
        msingle_field.errors = {}

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {})
        self.assertTrue(result)
        self.assertEqual(len(validator.errors), 0)

        validator = ErrorValidator()
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
        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {})
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 2)
        self.assertEqual(len(validator.errors.get('A')), 1)
        self.assertEqual(len(validator.errors.get('B')), 2)

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {'B': 'Them'}, update=True)
        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 2)
        self.assertEqual(len(validator.errors.get('A')), 1)
        self.assertEqual(len(validator.errors.get('B')), 3)










