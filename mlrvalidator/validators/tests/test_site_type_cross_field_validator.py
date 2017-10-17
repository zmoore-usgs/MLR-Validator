from unittest import TestCase, mock

from ..site_type_cross_field_validator import SiteTypeCrossFieldValidator

@mock.patch('mlrvalidator.validators.site_type_cross_field_reference.get_site_type_field_dependencies')
class SiteTypeCrossFieldValidatorSiteTypeFieldTestCase(TestCase):

    def setUp(self):

        self.validator = SiteTypeCrossFieldValidator(allow_unknown=True,
                                                     schema={'field1': {'validator': 'site_type_field'}})

    def test_with_null_attrs_for_site(self, mget_dep):
        mget_dep.return_value = {'siteTypeCode' : 'A', 'nullAttrs': ['field1'], 'notNullAttrs': ['field2']}
        self.assertTrue(self.validator.validate({'siteTypeCode': 'A', 'field1': '   '}, {}))
        self.assertFalse(self.validator.validate({'siteTypeCode': 'A', 'field1': 'B'}, {}))

    def test_with_not_null_attrs_for_site(self, mget_dep):
        mget_dep.return_value = {'siteTypeCode' : 'A', 'nullAttrs': ['field2'], 'notNullAttrs': ['field1']}
        self.assertTrue(self.validator.validate({'siteTypeCode': 'A', 'field1' : 'A'}, {}))
        self.assertFalse(self.validator.validate({'siteTypeCode': 'A', 'field1' : '  ' }, {}))

    def test_with_no_reference(self, mget_dep):
        mget_dep.return_value = {'siteTypeCode': 'A', 'nullAttrs': [],
                                                         'notNullAttrs': []}
        self.assertTrue(self.validator.validate({'siteTypeCode': 'A', 'field1' : 'A'}, {}))
        self.assertTrue(self.validator.validate({'siteTypeCode': 'A', 'field1': '   '}, {}))

    def test_with_null_attrs_for_site_update(self, mget_dep):
        mget_dep.return_value = {'siteTypeCode': 'A', 'nullAttrs': ['field1'], 'notNullAttrs': ['field2']}
        self.assertTrue(self.validator.validate({'field1': '  '}, {'siteTypeCode': 'A', 'field1': 'B'}, update=True))
        self.assertFalse(self.validator.validate({ 'field1': 'B'}, {'siteTypeCode': 'A','field1': '   '}, update=True))

    def test_with_not_null_attrs_for_site_update(self, mget_dep):
        mget_dep.return_value = {'siteTypeCode': 'A', 'nullAttrs': ['field2'], 'notNullAttrs': ['field1']}
        self.assertTrue(self.validator.validate({'field1': 'A'}, {'siteTypeCode': 'A', 'field1' : '  '}, update=True))
        self.assertFalse(self.validator.validate({'field1': '  '}, {'siteTypeCode': 'A', 'field1' : 'B'}, update=True))

    def test_with_no_reference_update(self, mget_dep):
        mget_dep.return_value = {'siteTypeCode': 'A', 'nullAttrs': [],
                                                         'notNullAttrs': []}
        self.assertTrue(self.validator.validate({'field1': 'A'}, {'siteTypeCode': 'A'}, update=True))
        self.assertTrue(self.validator.validate({'field1': '   '}, {'siteTypeCode': 'A'}, update=True))


@mock.patch('mlrvalidator.validators.site_type_cross_field_reference.get_site_type_field_dependencies')
class SiteTypeCrossFieldValidatorAllSiteTypeFields(TestCase):

    def setUp(self):
        self.validator = SiteTypeCrossFieldValidator(allow_unknown=True,
                                                     schema={'siteTypeCode': {'validator': 'all_site_type_fields'}}
                                                     )
        self.mock_site_type_ref = {
            'siteTypeCode' : 'A',
            'nullAttrs': ['field2', 'field3'], 'notNullAttrs': ['field1', 'field4']
        }

    def test_valid_all_fields(self, mget_dep):
        mget_dep.return_value = self.mock_site_type_ref
        self.assertTrue(self.validator.validate(
            {'siteTypeCode': 'A', 'field1': 'B', 'field4': 'C'},
            {}
        ))
        self.assertTrue(self.validator.validate(
            {'siteTypeCode': 'A', 'field1': 'B', 'field2': '   ', 'field3': '   ', 'field4': 'C'},
            {}
        ))

    def test_invalid_all_fields(self, mget_dep):
        mget_dep.return_value = self.mock_site_type_ref
        self.assertFalse(self.validator.validate(
            {'siteTypeCode': 'A', 'field1': 'B'},
            {}
        ))
        errors = self.validator.errors.get('siteTypeCode')[0]
        self.assertNotIn('field1', errors)
        self.assertIn('field4', errors)

        self.assertFalse(self.validator.validate(
            {'siteTypeCode': 'A', 'field1': 'B', 'field2': 'C', 'field3': 'D', 'field4' : 'E'},
            {}
        ))
        errors = self.validator.errors.get('siteTypeCode')[0]
        self.assertNotIn('field1', errors)
        self.assertIn('field2', errors)
        self.assertIn('field3', errors)
        self.assertNotIn('field4', errors)

        self.assertFalse(self.validator.validate(
            {'siteTypeCode': 'A', 'field1': ' ', 'field2': 'C', 'field3': ' ', 'field4': 'E'},
            {}
        ))
        errors = self.validator.errors.get('siteTypeCode')[0]
        self.assertIn('field1', errors)
        self.assertIn('field2', errors)
        self.assertNotIn('field3', errors)
        self.assertNotIn('field4', errors)


    def test_valid_all_fields_update(self, mget_dep):
        mget_dep.return_value = self.mock_site_type_ref
        self.assertTrue(self.validator.validate(
            {'siteTypeCode': 'A', 'field1': 'B', 'field4': 'C'},
            {'field2' : '  ', 'field4': ' '},
            update=True
        ))
        self.assertTrue(self.validator.validate(
            {'siteTypeCode': 'A', 'field2': '   ', 'field4': 'C'},
            {'field1': 'B', 'field3': '   '},
            update=True
        ))

    def test_invalid_all_fields_update(self, mget_dep):
        mget_dep.return_value = self.mock_site_type_ref
        self.assertFalse(self.validator.validate(
            {'siteTypeCode': 'A', },
            {'field1': 'B'},
            update=True
        ))
        errors = self.validator.errors.get('siteTypeCode')[0]
        self.assertNotIn('field1', errors)
        self.assertNotIn('field2', errors)
        self.assertNotIn('field3', errors)
        self.assertIn('field4', errors)

        self.assertFalse(self.validator.validate(
            {'siteTypeCode': 'A', 'field1': 'B', 'field2': 'C', 'field4': 'E'},
            {'field2': '   ', 'field3': 'F'},
            update=True
        ))
        errors = self.validator.errors.get('siteTypeCode')[0]
        self.assertNotIn('field1', errors)
        self.assertIn('field2', errors)
        self.assertIn('field3', errors)
        self.assertNotIn('field4', errors)

        self.assertFalse(self.validator.validate(
            {'siteTypeCode': 'A', 'field2': 'C', 'field3': ' '},
            {'field1': ' ', 'field4': 'E'},
            update=True
        ))
        errors = self.validator.errors.get('siteTypeCode')[0]
        self.assertIn('field1', errors)
        self.assertIn('field2', errors)
        self.assertNotIn('field3', errors)
        self.assertNotIn('field4', errors)

