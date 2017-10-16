
from unittest import TestCase, mock

from ..error_validator import ErrorValidator

@mock.patch('mlrvalidator.validators.error_validator.CrossFieldValidator')
@mock.patch('mlrvalidator.validators.error_validator.SiteTypeCrossFieldValidator')
@mock.patch('mlrvalidator.validators.error_validator.ReferenceValidator')
@mock.patch('mlrvalidator.validators.error_validator.SingleFieldValidator')
class ErrorValidatorErrorsTestCase(TestCase):

    def test_all_valid(self, msingle_field_class, mreference_class, msitetype_class, mcrossfield_class):
        msingle_field = msingle_field_class.return_value
        mreference = mreference_class.return_value
        msitetype = msitetype_class.return_value
        mcrossfield = mcrossfield_class.return_value

        msingle_field.validate.return_value = True
        msingle_field.errors = {}
        mreference.validate.return_value = True
        mreference.errors = {}
        msitetype.validate.return_value = True
        msitetype.errors = {}
        mcrossfield.validate.return_value = True
        mcrossfield.errors = {}

        validator = ErrorValidator()
        result = validator.validate({'A' : 'This', 'B' : 'That'}, {})

        self.assertTrue(result)
        self.assertEqual(len(validator.errors), 0)

    def test_single_field_invalid(self, msingle_field_class, mreference_class, msitetype_class, mcrossfield_class):
        msingle_field = msingle_field_class.return_value
        mreference = mreference_class.return_value
        msitetype = msitetype_class.return_value
        mcrossfield = mcrossfield_class.return_value

        msingle_field.validate.return_value = False
        msingle_field.errors = {'A' : ['Invalid']}
        mreference.validate.return_value = True
        mreference.errors = {}
        msitetype.validate.return_value = True
        msitetype.errors = {}
        mcrossfield.validate.return_value = True
        mcrossfield.errors = {}

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {})

        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)

    def test_reference_invalid(self, msingle_field_class, mreference_class, msitetype_class, mcrossfield_class):
        msingle_field = msingle_field_class.return_value
        mreference = mreference_class.return_value
        msitetype = msitetype_class.return_value
        mcrossfield = mcrossfield_class.return_value

        msingle_field.validate.return_value = True
        msingle_field.errors = {}
        mreference.validate.return_value = False
        mreference.errors = {'A': ['Invalid']}
        msitetype.validate.return_value = True
        msitetype.errors = {}
        mcrossfield.validate.return_value = True
        mcrossfield.errors = {}

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {})

        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)

    def test_sitetype_invalid(self, msingle_field_class, mreference_class, msitetype_class, mcrossfield_class):
        msingle_field = msingle_field_class.return_value
        mreference = mreference_class.return_value
        msitetype = msitetype_class.return_value
        mcrossfield = mcrossfield_class.return_value

        msingle_field.validate.return_value = True
        msingle_field.errors = {}
        mreference.validate.return_value = True
        mreference.errors = {}
        msitetype.validate.return_value = False
        msitetype.errors = {'A': ['Invalid']}
        mcrossfield.validate.return_value = True
        mcrossfield.errors = {}

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {})

        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)

    def test_crossfield_invalid(self, msingle_field_class, mreference_class, msitetype_class, mcrossfield_class):
        msingle_field = msingle_field_class.return_value
        mreference = mreference_class.return_value
        msitetype = msitetype_class.return_value
        mcrossfield = mcrossfield_class.return_value

        msingle_field.validate.return_value = True
        msingle_field.errors = {}
        mreference.validate.return_value = True
        mreference.errors = {}
        msitetype.validate.return_value = True
        msitetype.errors = {}
        mcrossfield.validate.return_value = False
        mcrossfield.errors = {'A': ['Bad']}

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {})

        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 1)

    def test_multiple_invalid(self, msingle_field_class, mreference_class, msitetype_class, mcrossfield_class):
        msingle_field = msingle_field_class.return_value
        mreference = mreference_class.return_value
        msitetype = msitetype_class.return_value
        mcrossfield = mcrossfield_class.return_value

        msingle_field.validate.return_value = False
        msingle_field.errors = {'B': ['Invalid']}
        mreference.validate.return_value = False
        mreference.errors = {'A': ['Bad']}
        msitetype.validate.return_value = True
        msitetype.errors = {}
        mcrossfield.validate.return_value = False
        mcrossfield.errors = {'A': ['Invalid']}

        validator = ErrorValidator()
        result = validator.validate({'A': 'This', 'B': 'That'}, {})

        self.assertFalse(result)
        self.assertEqual(len(validator.errors), 2)


class ErrorValidatorLatitudeTestCase(TestCase):

    def latitude_without_longitude_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 0400000'}, {}))








