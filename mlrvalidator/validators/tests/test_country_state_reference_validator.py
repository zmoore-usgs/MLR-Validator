
import json
from unittest import TestCase, mock

from ..country_state_reference_validator import CountryStateReferenceValidator

class CountryStateReferenceValidatorTestCase(TestCase):

    def setUp(self):
        ref_list = {
            "countries": [
                {
                    "countryCode": "BG",
                    "states": [
                        {
                            "stateFipsCode": "00",
                            "aquiferCodes": [
                                "200CRSL"
                            ]
                        }
                    ]
                }, {
                    "countryCode": "US",
                    "states": [
                        {
                            "stateFipsCode": "01",
                            "aquiferCodes": [
                                "100CNZC",
                                "110QRNR"
                            ]
                        }, {

                            "stateFipsCode": "02",
                            "aquiferCodes": [
                                "000MCRL",
                                "000SELS"
                            ]
                        }
                    ]
                }
            ]
        }
        with mock.patch('mlrvalidator.validators.reference.open', mock.mock_open(read_data=json.dumps(ref_list)), create=True):
            self.validator = CountryStateReferenceValidator('fake_file', 'aquiferCodes', 'aquiferCode')

    def test_valid_value_in_list(self):
        self.assertTrue(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '01', 'aquiferCode': '110QRNR'}, {}))
        self.assertEqual(self.validator.errors, {})

        self.assertTrue(self.validator.validate({'countryCode': 'US'}, {'stateFipsCode': '01', 'aquiferCode': '110QRNR'}))
        self.assertEqual(self.validator.errors, {})

        self.assertTrue(self.validator.validate({'countryCode': 'US', 'aquiferCode': '110QRNR'}, {'stateFipsCode': '01', 'aquiferCode': '112QRNR'}))
        self.assertEqual(self.validator.errors, {})

    def test_valid_if_any_missing_keys(self):
        self.assertTrue(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '01'}, {}))
        self.assertTrue(self.validator.validate({'countryCode': 'US'}, { 'aquiferCode': '110QRNR'}))
        self.assertTrue(self.validator.validate({'stateFipsCode': '01', 'aquiferCode': '110QRNR'}, {}))

    def test_bad_lookup(self):
        self.assertFalse(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '01', 'aquiferCode': 'A'}, {}))
        self.assertNotEqual(self.validator.errors, {})

        self.assertFalse(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '01', 'aquiferCode': 'A'}, {'aquiferCode': '110QRNR'}))
        self.assertNotEqual(self.validator.errors, {})

