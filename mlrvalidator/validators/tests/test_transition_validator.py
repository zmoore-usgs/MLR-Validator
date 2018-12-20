
import json
from unittest import TestCase, mock

from ..transition_validator import TransitionValidator

class TransitionValidatorSiteTypeTestCase(TestCase):

    @mock.patch('mlrvalidator.validators.transition_validator.SiteTypeInvalidCodes')
    @mock.patch('mlrvalidator.validators.transition_validator.FieldTransitions')
    def setUp(self, mfield_transitions, msite_type_invalid_codes):
    
        msite_type_invalid_codes.return_value.get_site_type_invalid_codes.return_value = ['FA', 'SS']
        mfield_transitions.return_value.get_allowed_transitions.return_value = ['FA-SPS', 'FA-WIW', 'FA-DV', 'FA-OF']
        self.validator = TransitionValidator('ref_dir')

    def test_valid_transition(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-DV'}, {'siteTypeCode': 'AS'}))

    def test_invalid_transition(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'SP'}, {'siteTypeCode': 'AS'}))

    def test_missing_field(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-DV'}, {}))
        self.assertTrue(self.validator.validate({}, {'siteTypeCode': 'AG'}))

    def test_existing_not_in_ref_list(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-DV'}, {'siteTypeCode': 'AB'}))

    def test_no_change_from_existing_to_new(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'AG'}, {'siteTypeCode': 'AG'}))

    def test_invalid_site_type_transition(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'FA'}, {'siteTypeCode': 'FA'}))
        self.assertFalse(self.validator.validate({'siteTypeCode': 'SS'}, {'siteTypeCode': 'SS'}))