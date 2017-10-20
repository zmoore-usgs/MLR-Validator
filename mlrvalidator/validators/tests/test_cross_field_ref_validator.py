
import json
from unittest import TestCase, mock

from ..cross_field_ref_validator import CrossFieldRefValidator


class TestCrossFieldRefValidatorForStates(TestCase):

    def setUp(self):
        ref_list = {
            "countries": [
                {
                    "countryCode": "AF",
                    "states": [
                        {
                            "stateFipsCode": "00",
                            "state_min_lat_va": "292900",
                            "state_max_lat_va": "383000",
                            "state_min_long_va": "-0745800",
                            "state_max_long_va": "-0605000",
                            "state_min_alt_va": "00000",
                            "state_max_alt_va": "30000"
                        }
                    ]
                }, {

                    "countryCode": "US",
                    "states": [
                        {
                            "stateFipsCode": "00",
                            "state_min_lat_va": "-900000",
                            "state_max_lat_va": "900000",
                            "state_min_long_va": "-1800000",
                            "state_max_long_va": "1800000",
                            "state_min_alt_va": "-282",
                            "state_max_alt_va": "20320"
                        },
                        {
                            "stateFipsCode": "01",
                            "state_min_lat_va": "300840",
                            "state_max_lat_va": "350029",
                            "state_min_long_va": "0845318",
                            "state_max_long_va": "0882824",
                            "state_min_alt_va": "00000",
                            "state_max_alt_va": "02407"
                        }
                    ]
                }
            ]
        }
        with mock.patch(
                'mlrvalidator.validators.cross_field_ref_validator.CountryStateReferenceValidator') as mref_validator_class:
            with mock.patch('mlrvalidator.validators.reference.open',
                            mock.mock_open(read_data=json.dumps(ref_list))):
                mref_validator = mref_validator_class.return_value
                mref_validator.validate.return_value = True
                mref_validator.errors = None


                self.validator = CrossFieldRefValidator('ref_dir')

    def test_state_not_in_list(self):
        self.assertFalse(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '02'}, {}))
        self.assertEqual(len(self.validator.errors), 1)

        self.assertFalse(self.validator.validate({'countryCode': 'US'}, {'stateFipsCode': '02'}))
        self.assertEqual(len(self.validator.errors), 1)

        self.assertFalse(self.validator.validate({'stateFipsCode': '02'}, {'countryCode': 'US' }))
        self.assertEqual(len(self.validator.errors), 1)

    def test_state_in_list(self):
        self.assertTrue(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '01'}, {}))
        self.assertEqual(len(self.validator.errors), 0)

        self.assertTrue(self.validator.validate({'countryCode': 'US'}, {'stateFipsCode': '01'}))
        self.assertEqual(len(self.validator.errors), 0)

        self.assertTrue(self.validator.validate({'stateFipsCode': '01'}, {'countryCode': 'US'}))
        self.assertEqual(len(self.validator.errors), 0)

    def test_missing_state(self):
        self.assertTrue(self.validator.validate({'countryCode': 'US'}, {}))
        self.assertEqual(len(self.validator.errors), 0)

        self.assertTrue(self.validator.validate({}, {'countryCode': 'US'}))
        self.assertEqual(len(self.validator.errors), 0)

    def test_missing_country(self):
        self.assertTrue(self.validator.validate({'stateFipsCode': '01'}, {}))
        self.assertEqual(len(self.validator.errors), 0)

        self.assertTrue(self.validator.validate({}, {'stateFipsCode': '01'}))
        self.assertEqual(len(self.validator.errors), 0)


