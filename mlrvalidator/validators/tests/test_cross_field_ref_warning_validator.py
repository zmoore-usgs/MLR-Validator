
import json
import unittest
from unittest import TestCase, mock

from ..cross_field_ref_warning_validator import CrossFieldRefWarningValidator


class CrossFieldRefWarningCountyLatitudeTestCase(TestCase):
    @mock.patch('mlrvalidator.validators.cross_field_ref_warning_validator.States')
    def setUp(self, mstates_ref):
        ref_list = ref_list = {
            "countries": [
                {
                    "countryCode": "AF",
                    "states": [
                        {
                            "stateFipsCode": "00",
                            "counties": [
                                {
                                    "countyCode": "000",
                                    "county_min_lat_va": "292900",
                                    "county_max_lat_va": "383000",
                                    "county_min_long_va": "-0745800",
                                    "county_max_long_va": "-0605000",
                                    "county_min_alt_va": "00000",
                                    "county_max_alt_va": "30000"
                                }
                            ]
                        }
                    ]
                }, {
                    "countryCode": "CA",
                    "states": [
                        {
                            "stateFipsCode": "00",
                            "counties": [
                                {
                                    "countyCode": "000",
                                    "county_min_lat_va": "414036",
                                    "county_max_lat_va": "694000",
                                    "county_min_long_va": "0553000",
                                    "county_max_long_va": "1410000",
                                    "county_min_alt_va": "00000",
                                    "county_max_alt_va": "30000"
                                }
                            ]
                        }, {
                            "stateFipsCode": "90",
                            "counties": [
                                {
                                    "countyCode": "000",
                                    "county_min_lat_va": "443000",
                                    "county_max_lat_va": "480500",
                                    "county_min_long_va": "0634500",
                                    "county_max_long_va": "0690500",
                                    "county_min_alt_va": "00000",
                                    "county_max_alt_va": "02690"
                                }, {
                                    "countyCode": "001",
                                    "county_min_lat_va": "414036",
                                    "county_max_lat_va": "694000",
                                    "county_min_long_va": "0553000",
                                    "county_max_long_va": "1410000",
                                    "county_min_alt_va": "00000",
                                    "county_max_alt_va": "30000"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefWarningValidator('ref_dir')

    def test_valid_latitude_range(self):
        self.assertTrue(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90', 'countyCode': '001', 'latitude': ' 500000'}, {}))

    def test_invalid_latitude_range(self):
        self.assertFalse(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90', 'countyCode': '001', 'latitude': ' 300000'}, {}))

    def test_missing_fields(self):
        self.assertTrue(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90', 'countyCode': '    ', 'latitude': ' 500000'}, {}))

    def test_missing_reference(self):
            self.assertTrue(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90', 'countyCode': '010', 'latitude': ' 300000'}, {}))


class CrossFieldRefWarningCountyLongitudeTestCase(TestCase):
    @mock.patch('mlrvalidator.validators.cross_field_ref_warning_validator.States')
    def setUp(self, mstates_ref):
        ref_list = ref_list = {
            "countries": [
                {
                    "countryCode": "AF",
                    "states": [
                        {
                            "stateFipsCode": "00",
                            "counties": [
                                {
                                    "countyCode": "000",
                                    "county_min_lat_va": "292900",
                                    "county_max_lat_va": "383000",
                                    "county_min_long_va": "-0745800",
                                    "county_max_long_va": "-0605000",
                                    "county_min_alt_va": "00000",
                                    "county_max_alt_va": "30000"
                                }
                            ]
                        }
                    ]
                }, {
                    "countryCode": "CA",
                    "states": [
                        {
                            "stateFipsCode": "00",
                            "counties": [
                                {
                                    "countyCode": "000",
                                    "county_min_lat_va": "414036",
                                    "county_max_lat_va": "694000",
                                    "county_min_long_va": "0553000",
                                    "county_max_long_va": "1410000",
                                    "county_min_alt_va": "00000",
                                    "county_max_alt_va": "30000"
                                }
                            ]
                        }, {
                            "stateFipsCode": "90",
                            "counties": [
                                {
                                    "countyCode": "000",
                                    "county_min_lat_va": "443000",
                                    "county_max_lat_va": "480500",
                                    "county_min_long_va": "0634500",
                                    "county_max_long_va": "0690500",
                                    "county_min_alt_va": "00000",
                                    "county_max_alt_va": "02690"
                                }, {
                                    "countyCode": "001",
                                    "county_min_lat_va": "414036",
                                    "county_max_lat_va": "694000",
                                    "county_min_long_va": "0553000",
                                    "county_max_long_va": "1410000",
                                    "county_min_alt_va": "00000",
                                    "county_max_alt_va": "30000"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefWarningValidator('ref_dir')

    def test_missing_fields(self):
        self.assertTrue(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90', 'countyCode': '    ', 'longitude': ' 1000000'}, {}))

    def test_missing_reference(self):
            self.assertTrue(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90', 'countyCode': '010', 'longitude': ' 1000000'}, {}))

    def test_valid_latitude_range(self):
        self.assertTrue(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '90', 'countyCode': '001', 'longitude': ' 1000000'}, {}))

    def test_invalid_latitude_range(self):
        self.assertFalse(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90', 'countyCode': '001', 'longitude': ' 0100000'}, {}))



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

    def test_nonnumeric_altitude(self):
        self.assertTrue(self.validator.validate({'altitude': 'N19'},{'stateFipsCode': '33', 'countryCode': 'US'}))

class CrossFieldRefWarningUseCodeTestCase(TestCase):

    def setUp(self):
        ref_list = {
            "siteUseCodes": [
                {
                    'primaryUseOfSiteCode': 'A',
                    'secondaryUseOfSiteCode': ['A', 'B'],
                    'tertiaryUseOfSiteCode': ['A', 'B', 'C']
                },
                ],
            "waterUseCodes": [
                {
                    'primaryUseOfWaterCode': 'A',
                    'secondaryUseOfWaterCode': ['A', 'B'],
                    'tertiaryUseOfWaterCode': ['A', 'B', 'C']
                }
            ]
        }
        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefWarningValidator('ref_dir')
        self.site_lists = [['primaryUseOfSiteCode', 'secondaryUseOfSiteCode', 'tertiaryUseOfSiteCode'],
                      ['primaryUseOfWaterCode', 'secondaryUseOfWaterCode', 'tertiaryUseOfWaterCode']]

    def test_unique_use_codes(self):
        for sites in self.site_lists:
            self.assertTrue(self.validator.validate({sites[0]: 'A', sites[1]: 'B', sites[2]: 'C'}, {}))

    def test_non_unique_use_codes(self):
        for sites in self.site_lists:
            self.assertFalse(self.validator.validate({sites[0]: 'A', sites[1]: 'A', sites[2]: 'A'}, {}))
            self.assertFalse(self.validator.validate({sites[0]: 'A', sites[1]: 'A', sites[2]: 'C'}, {}))
            self.assertFalse(self.validator.validate({sites[0]: 'A', sites[1]: 'B', sites[2]: 'A'}, {}))
            self.assertFalse(self.validator.validate({sites[0]: 'A', sites[1]: 'B', sites[2]: 'B'}, {}))

class CrossFieldValidatorSiteNumberFieldTestCase(TestCase):
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.CountryStateReferenceValidator')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.States')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.LandNetCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.SiteTypesCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.NationalWaterUseCodes')
    def setUp(self, mwater_use_ref, mland_net_ref, msite_type_ref, mstates_ref, mref_validator_class):
        ref_list = {
            "siteNumberFormatCodes": [
            {
                "siteNumberFormatCode": "LL",
                "siteTypeCode": [
                    "AT"
                    ]
            },
            {
                  "siteNumberFormatCode": "DSLL",
                  "siteTypeCode": [
                    "GL"
                    ]
            },
            {
                 "siteNumberFormatCode": "WU",
                 "siteTypeCode": [
                    "AW"
                    ]
            },
            {
                "siteNumberFormatCode": "LLWU",
                "siteTypeCode": [
                    "FA-CI"
                ]
            }
            ]
        }
        mref_validator = mref_validator_class.return_value
        mref_validator.validate.return_value = True
        mref_validator.errors = []

        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefWarningValidator('ref_dir')

    def test_no_site_number_valid(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'AT', 'siteNumber': ' '}, {}))

    def test_no_site_type_valid(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': ' ', 'siteNumber': '12345678'}, {}))

    def test_site_number_ll_valid(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'AT', 'siteNumber': '012345678901234'}, {}))

    def test_site_number_dsll_min_length_valid(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'GL', 'siteNumber': '12345678'}, {}))

    def test_site_number_dsll_max_length_valid(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'GL', 'siteNumber': '012345678901234'}, {}))

    def test_site_number_wu_min_length_first_digit_valid(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'AW', 'siteNumber': '9876543210'}, {}))

    def test_site_number_wu_max_length_first_digit_valid(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'AW', 'siteNumber': '987654321098765'}, {}))

    def test_site_number_llwu_max_length_first_digit_valid(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '987654321098765'}, {}))

    def test_site_number_llwu_max_length_valid(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '087654321098765'}, {}))

    def test_site_number_llwu_min_length_valid(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '9876543210'}, {}))

    def test_site_number_ll_invalid(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'AT', 'siteNumber': '01234567890123'}, {}))

    def test_site_number_dsll_less_than_min_length_invalid(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'GL', 'siteNumber': '1234567'}, {}))

    def test_site_number_dsll_greater_than_max_length_invalid(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'GL', 'siteNumber': '0123456789012345'}, {}))

    def test_site_number_wu_less_than_min_length_first_digit_invalid(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'AW', 'siteNumber': '987654321'}, {}))

    def test_site_number_wu_no_first_digit_invalid(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'AW', 'siteNumber': '8765432109'}, {}))

    def test_site_number_wu_greater_than_max_length_first_digit_invalid(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'AW', 'siteNumber': '987654321098765432'}, {}))

    def test_site_number_llwu_greater_than_max_length_invalid(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '98765432109876543'}, {}))

    def test_site_number_llwu_less_than_min_length_invalid(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '59876543'}, {}))

    def test_site_number_llwu_wrong_first_digit_invalid(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '087654321098'}, {}))

