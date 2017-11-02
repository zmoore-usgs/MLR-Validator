
from unittest import TestCase

from ..cross_field_warning_validator import CrossFieldWarningValidator

class DrainageAreaTestCase(TestCase):

    def setUp(self):
        self.validator = CrossFieldWarningValidator()

    def test_contributing_drainage_area_equal_to_drainage_area(self):
        self.assertFalse(self.validator.validate({'contributingDrainageArea': '10', 'drainageArea': '10'}, {}))
        self.assertFalse(self.validator.validate({'contributingDrainageArea': '10.1', 'drainageArea': '10.1'}, {}))

    def test_contributing_drainage_area_not_equal_to_drainage_area(self):
        self.assertTrue(self.validator.validate({'contributingDrainageArea': '11', 'drainageArea': '10'}, {}))
        self.assertTrue(self.validator.validate({'contributingDrainageArea': '10', 'drainageArea': '11'}, {}))

    def test_missing_drainage_areas(self):
        self.assertTrue(self.validator.validate({'contributingDrainageArea': '11', 'drainageArea': '  '}, {}))
        self.assertTrue(self.validator.validate({'drainageArea': '10'}, {}))