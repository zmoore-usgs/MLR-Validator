from unittest import TestCase
from ..cross_field_validator import CrossFieldValidator
from mlrvalidator.schema import cross_field_schema


class CrossFieldValidatorReciprocalDependencyTestCase(TestCase):
    def setUp(self):
        self.validator = CrossFieldValidator(allow_unknown=True, schema={'field1': {'reciprocal_dependency': ['field2', 'field3']}})

    def test_missing_field_dependency(self):
        self.assertFalse(self.validator.validate({'field1': ' 1000000'}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 2)

        self.assertFalse(self.validator.validate({'field1': ' 1000000', 'field2': 'B'}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1': ' 1000000', 'field3': 'B'}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)


    def test_null_field_dependency(self):
        self.assertFalse(self.validator.validate({'field1' : '11111', 'field2': '      ', 'field3' : 'B'}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1' : '11111', 'field2': 'B', 'field3' : '    '}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1' : '11111', 'field2' : '    ', 'field3' : '  '}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 2)


    def test_valid_field_dependency(self):
        self.assertTrue(self.validator.validate({'field1': '11111', 'field2': '22222', 'field3': 'B'}, {}))

    def test_update_missing_field_dependency(self):
        self.assertFalse(self.validator.validate({'field1': ' 1000000'}, {}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 2)

        self.assertFalse(self.validator.validate({'field1': ' 1000000', }, {'field2': 'A'}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1': ' 1000000'}, {'field3': 'A'}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

    def test_update_null_field_dependency(self):
        self.assertFalse(self.validator.validate({'field1': ' 1000000', 'field2': '      '}, {'field3': 'B'}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1': ' 1000000'}, {'field2': '      ', 'field3': 'B'}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1': ' 1000000'}, {'field2': '      ', 'field3': ' '}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 2)


    def test_update_valid_field_dependency(self):
        self.assertTrue(self.validator.validate({'field1': '11111', 'field2': '2222'}, {'field2': '    ', 'field3': 'B'}, update=True))
        self.assertTrue(self.validator.validate({'field1': '11111', 'field3': '22222'}, {'field2' : 'A'}, update=True))


class CrossFieldValidatorUniqueUseTestCase(TestCase):

    def setUp(self):
        self.validator = CrossFieldValidator(allow_unknown=True, schema={'field1': {'unique_use_value': ['field2', 'field3']}})

    def test_valid_unique_use(self):
        self.assertTrue(self.validator.validate({'field1': 'A', 'field2': 'B', 'field3' : 'B'}, {}))
        self.assertTrue(self.validator.validate({'field1': 'A', 'field2': ' '}, {}))
        self.assertTrue(self.validator.validate({'field1': ' ', 'field2': 'B'}, {}))
        self.assertTrue(self.validator.validate({'field1': ' '}, {}))

    def test_not_unique_use(self):
        self.assertFalse(self.validator.validate({'field1': 'A', 'field2': 'A'}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1': 'A', 'field2': 'A', 'field3': 'A'}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 2)


    def test_valid_unique_use_on_update(self):
        self.assertTrue(self.validator.validate({'field1': 'A', 'field3': 'B'}, {'field2': 'B'}, update=True))
        self.assertTrue(self.validator.validate({'field1': ' '}, {'field2': 'B'}, update=True))
        self.assertTrue(self.validator.validate({'field1': ' '}, {'field2': ' '}, update=True))

    def test_not_unique_use_on_update(self):
        self.assertFalse(self.validator.validate({'field1': 'A'}, {'field2': 'A'}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1': 'A', 'field2': 'A'}, {'field3': 'A'}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 2)


class CrossFieldValidatorNotEmptyDependencyTestCase(TestCase):

    def setUp(self):
        self.validator = CrossFieldValidator(allow_unknown=True, schema={'field1': {'not_empty_dependency' : ['field2', 'field3']}})

    def test_valid_not_empty_dependency(self):
        self.assertTrue(self.validator.validate({'field1' : 'A', 'field2': 'B', 'field3': 'C'}, {}))
        self.assertTrue(self.validator.validate({'field1': ' ', 'field2': 'B', 'field3': 'C'}, {}))

    def test_invalid_not_empty_dependency(self):
        self.assertFalse(self.validator.validate({'field1': 'A', 'field2': ' ', 'field3': 'C'}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1': 'A', 'field2': 'B'}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1': 'A', 'field3': ' '}, {}))
        self.assertEqual(len(self.validator.errors.get('field1')), 2)

    def test_valid_not_empty_dependency_on_update(self):
        self.assertTrue(self.validator.validate({'field1' : 'A', 'field2': 'B', }, {'field3': 'C'}, update=True))
        self.assertTrue(self.validator.validate({'field1' : ' ', 'field2': 'B', }, {'field3': 'C'}, update=True))

    def test_invalid_not_empty_dependency(self):
        self.assertFalse(self.validator.validate({'field1': 'A'}, {'field3': 'C'}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1': 'A', 'field2': 'B'}, {'field3': ' '}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 1)

        self.assertFalse(self.validator.validate({'field1': 'A'}, {'field2': ' ', 'field3': ' '}, update=True))
        self.assertEqual(len(self.validator.errors.get('field1')), 2)


class CrossFieldValidatorContructionBeforeInventoryTestCase(TestCase):

    def setUp(self):
        self.validator = CrossFieldValidator(allow_unknown=True,
                                             schema={'firstConstructionDate' : {'construction_before_inventory': True},
                                                     'siteEstablishmentDate' : {'construction_before_inventory': True}})

    def test_valid_date(self):
        self.assertTrue(self.validator.validate({'firstConstructionDate': '20100415', 'siteEstablishmentDate': '20100416'}, {}))
        self.assertTrue(self.validator.validate({'firstConstructionDate': '201004', 'siteEstablishmentDate': '20100416'}, {}))
        self.assertTrue(self.validator.validate({'firstConstructionDate': '2010', 'siteEstablishmentDate': '20100416'}, {}))
        self.assertTrue(self.validator.validate({'firstConstructionDate': '2010', 'siteEstablishmentDate': '201004'}, {}))

    def test_with_empty_date(self):
        self.assertTrue(self.validator.validate({'firstConstructionDate': '20100415'}, {}))
        self.assertTrue(self.validator.validate({'siteEstablishmentDate': '20100415'}, {}))

    def test_with_invalid_dates(self):
        self.assertFalse(self.validator.validate({'firstConstructionDate': '20100415', 'siteEstablishmentDate': '20100414'}, {}))
        self.assertFalse(self.validator.validate({'firstConstructionDate': '201004', 'siteEstablishmentDate': '20100315'}, {}))
        self.assertFalse(self.validator.validate({'firstConstructionDate': '2010', 'siteEstablishmentDate': '20091231'}, {}))

    def test_valid_date_with_update(self):
        self.assertFalse(self.validator.validate({'firstConstructionDate': '201004'}, {'siteEstablishmentDate': '20100315'}, update=True))
        self.assertFalse(self.validator.validate({'siteEstablishmentDate': '20100315'}, {'firstConstructionDate': '201004'}, update=True))

    def test_with_empty_date_update(self):
        self.assertTrue(self.validator.validate({'firstConstructionDate': '20100415'}, {'siteEstablishmentDate': ''}, update=True))
        self.assertTrue(self.validator.validate({'siteEstablishmentDate': '20100415'}, {'firstConstructionDate': ''}, update=True))

    def test_with_invalid_dates_update(self):
        self.assertFalse(self.validator.validate({'firstConstructionDate': '20100415'}, {'siteEstablishmentDate': '20100414'}, update=True))
        self.assertFalse(self.validator.validate({'siteEstablishmentDate': '20100315'}, {'firstConstructionDate': '201004'}, update=True))

class CrossFieldValidatorCheckWellHoleDepthTestCase(TestCase):

    def setUp(self):
        self.validator = CrossFieldValidator(allow_unknown=True,
                                             schema={'wellDepth' : {'check_well_hole_depths': True},
                                                     'holeDepth' : {'check_well_hole_depths': True}})

    def test_valid_depths(self):
        self.assertTrue(self.validator.validate({'wellDepth': '1234', 'holeDepth': '11234'},  {}))
        self.assertTrue(self.validator.validate({'wellDepth': '9', 'holeDepth': '10'}, {}))

    def test_with_empty_depths(self):
        self.assertTrue(self.validator.validate({'wellDepth': '1234'}, {}))
        self.assertTrue(self.validator.validate({'holeDepth': '11234'}, {}))
        self.assertTrue(self.validator.validate({'wellDepth': ' ', 'holeDepth': ' '}, {}))
        self.assertTrue(self.validator.validate({'wellDepth' : '1234', 'holeDepth': 'A'}, {}))

    def test_invalid_depths(self):
        self.assertFalse(self.validator.validate({'wellDepth': '11234', 'holeDepth': '1234'}, {}))
        self.assertFalse(self.validator.validate({'wellDepth': '10', 'holeDepth': '9'}, {}))

    def test_valid_depths_update(self):
        self.assertTrue(self.validator.validate({'wellDepth': '1234'}, {'holeDepth': '11234'}, update=True))
        self.assertTrue(self.validator.validate({'holeDepth': '10'}, {'wellDepth': '9'}, update=True))

    def test_with_empty_depths_update(self):
        self.assertTrue(self.validator.validate({'wellDepth': '1234'}, {'holeDepth': '   '}, update=True))
        self.assertTrue(self.validator.validate({'holeDepth': '11234'}, {'wellDepth': '   '}, update=True))
        self.assertTrue(self.validator.validate({'wellDepth': ' ', 'holeDepth': ' '}, {}, update=True))
        self.assertTrue(self.validator.validate({'wellDepth': '1234', 'holeDepth': 'A'}, {}, update=True))

    def test_invalid_depths_update(self):
        self.assertFalse(self.validator.validate({'wellDepth': '11234'}, {'holeDepth': '1234'}, update=True))
        self.assertFalse(self.validator.validate({'holeDepth': '9'}, {'wellDepth': '10'}))



