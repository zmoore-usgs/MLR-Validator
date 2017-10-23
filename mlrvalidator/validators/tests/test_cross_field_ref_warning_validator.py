
import json

from unittest import TestCase, mock

from ..cross_field_ref_warning_validator import CrossFieldRefWarningValidator

class CrossFieldRefWarningLatitudeTestCase(TestCase):

    def setUp(self):
        ref_list = {
            'countries': [
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
                            "stateFipsCode": "02",
                            "state_min_lat_va": "511030",
                            "state_max_lat_va": "712628",
                            "state_min_long_va": "1295846",
                            "state_max_long_va": "-1722655",
                            "state_min_alt_va": "00000",
                            "state_max_alt_va": "20320"
                        }, {
                            "stateFipsCode": "34",
                            "state_min_lat_va": "384719",
                            "state_max_lat_va": "412127",
                            "state_min_long_va": "0735306",
                            "state_max_long_va": "0753349",
                            "state_min_alt_va": "00-10",
                            "state_max_alt_va": "01803"
                        }
                    ]
                }
            ]
        }
        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefWarningValidator('ref_dir')

    def test_valid_latitude(self):
        self.assertTrue(self.validator.validate({'latitude': ' 520000'}, {'stateFipsCode': '02', 'countryCode': 'US'}))

    def test_invalid_latitude(self):
        self.assertFalse(self.validator.validate({'latitude': ' 500000'}, {'stateFipsCode': '02', 'countryCode': 'US'}))

    def test_missing_fields(self):
        self.assertTrue(self.validator.validate({'latitude': ' 500000'}, {'stateFipsCode': '02'}))
        self.assertTrue(self.validator.validate({'latitude': ' 500000'}, {'countryCode': 'US'}))

    def test_missing_reference(self):
        self.assertTrue(self.validator.validate({'latitude': ' 500000'}, {'stateFipsCode': '02', 'countryCode': 'CN'}))


class CrossFieldRefWarningLongitudeTestCase(TestCase):

    def setUp(self):
        ref_list = {
            'countries': [
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
                            "stateFipsCode": "02",
                            "state_min_lat_va": "511030",
                            "state_max_lat_va": "712628",
                            "state_min_long_va": "1295846",
                            "state_max_long_va": "-1722655",
                            "state_min_alt_va": "00000",
                            "state_max_alt_va": "20320"
                        }, {
                            "stateFipsCode": "34",
                            "state_min_lat_va": "384719",
                            "state_max_lat_va": "412127",
                            "state_min_long_va": "0735306",
                            "state_max_long_va": "0753349",
                            "state_min_alt_va": "00-10",
                            "state_max_alt_va": "01803"
                        }
                    ]
                }
            ]
        }
        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefWarningValidator('ref_dir')

    def test_valid_latitude(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0740000'}, {'stateFipsCode': '34', 'countryCode': 'US'}))

    def test_invalid_latitude(self):
        self.assertFalse(self.validator.validate({'longitude': ' 0700000'}, {'stateFipsCode': '34', 'countryCode': 'US'}))

    def test_missing_fields(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0700000'}, {'stateFipsCode': '34'}))
        self.assertTrue(self.validator.validate({'longitude': ' 0700000'}, {'countryCode': 'US'}))

    def test_missing_reference(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0700000'}, {'stateFipsCode': '34', 'countryCode': 'CN'}))


class CrossFieldRefWarningAltitudeTestCase(TestCase):

    def setUp(self):
        ref_list = {
            'countries': [
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
                            "stateFipsCode": "02",
                            "state_min_lat_va": "511030",
                            "state_max_lat_va": "712628",
                            "state_min_long_va": "1295846",
                            "state_max_long_va": "-1722655",
                            "state_min_alt_va": "00000",
                            "state_max_alt_va": "20320"
                        }, {
                            "stateFipsCode": "34",
                            "state_min_lat_va": "384719",
                            "state_max_lat_va": "412127",
                            "state_min_long_va": "0735306",
                            "state_max_long_va": "0753349",
                            "state_min_alt_va": "00-10",
                            "state_max_alt_va": "01803"
                        }
                    ]
                }
            ]
        }
        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefWarningValidator('ref_dir')

    def test_valid_altitude(self):
        self.assertTrue(self.validator.validate({'altitude': '10000'}, {'stateFipsCode': '02', 'countryCode': 'US'}))
        self.assertTrue(self.validator.validate({'altitude': '-9'}, {'stateFipsCode': '34', 'countryCode': 'US'}))

    def test_invalid_altitude(self):
        self.assertFalse(self.validator.validate({'altitude': '30000'}, {'stateFipsCode': '02', 'countryCode': 'US'}))
        self.assertFalse(self.validator.validate({'altitude': '-19'}, {'stateFipsCode': '34', 'countryCode': 'US'}))

    def test_missing_fields(self):
        self.assertTrue(self.validator.validate({'altitude': '10000'}, {'stateFipsCode': '34'}))
        self.assertTrue(self.validator.validate({'altitude': '10000'}, {'countryCode': 'US'}))

    def test_missing_reference(self):
        self.assertTrue(self.validator.validate({'altitude': '-19'}, {'stateFipsCode': '34', 'countryCode': 'CN'}))
        self.assertTrue(self.validator.validate({'altitude': '-19'}, {'stateFipsCode': '33', 'countryCode': 'US'}))