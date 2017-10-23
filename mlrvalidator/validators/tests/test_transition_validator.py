
import json
from unittest import TestCase, mock

from ..transition_validator import TransitionValidator

class TransitionValidatorSiteTypeTestCase(TestCase):

    def setUp(self):
        ref_list = [
            {
                "existingField": "AG",
                "newFields": [
                    "FA-SPS",
                    "FA-WIW"
                ]
            }, {
                "existingField": "AS",
                "newFields": [
                    "FA-DV",
                    "FA-OF"
                ]
            }
        ]
        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = TransitionValidator('ref_dir')

    def test_valid_transition(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-DV'}, {'siteTypeCode': 'AS'}))

    def test_invalid_transition(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'FA-DV'}, {'siteTypeCode': 'AG'}))

    def test_missing_field(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-DV'}, {}))
        self.assertTrue(self.validator.validate({}, {'siteTypeCode': 'AG'}))

    def test_existing_not_in_ref_list(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-DV'}, {'siteTypeCode': 'AB'}))