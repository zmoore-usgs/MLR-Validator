
import json
import unittest
from unittest import TestCase, mock, skip

from ..cross_field_ref_error_validator import CrossFieldRefErrorValidator


class CrossFieldRefValidatorAllValidatorsTestCase(TestCase):
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.CountryStateReferenceValidator')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.NationalWaterUseCodes')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.States')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.SiteTypesCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.Counties')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.LandNetCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.SiteNumberFormat')
    def setUp(self, mcounties_ref, msite_type_ref, mstates_ref, mwater_use_ref, mland_net_ref, msite_number_ref, mref_validator_class):
        mref_validator = mref_validator_class.return_value
        mref_validator.validate.return_value = False
        mref_validator.errors = {'field1' : ['Error message']}
        self.validator = CrossFieldRefErrorValidator('ref_dir', 'ref_dir')

    def test_multiple_error(self):
        self.assertFalse(self.validator.validate({'dummyfield': 'A'}, {}))
        self.assertEqual(len(self.validator.errors), 1)


class CrossFieldRefValidatorForCountiesTestCase(TestCase):

    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.CountryStateReferenceValidator')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.NationalWaterUseCodes')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.SiteTypesCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.LandNetCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.SiteNumberFormat')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.States')
    def setUp(self, mstates_ref, msite_type_ref, mland_net_ref, msite_number_ref, mwater_use_ref, mref_validator_class):
        ref_list = {
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

        mref_validator = mref_validator_class.return_value
        mref_validator.validate.return_value = True
        mref_validator.errors = []

        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefErrorValidator('ref_dir', 'ref_dir')

    def test_county_not_in_list(self):
        self.assertFalse(self.validator.validate({'countryCode': 'CA', 'stateFipsCode' : '90', 'countyCode': '002'}, {}))

        self.assertFalse(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90'}, {'countyCode': '002'}))

    def test_state_not_in_list(self):
        self.assertFalse(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '80', 'countyCode': '002'}, {}))

        self.assertFalse(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '80'}, {'countyCode': '002'}))

    def test_country_not_in_list(self):
        self.assertFalse(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '80', 'countyCode': '002'}, {}))

        self.assertFalse(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '80'}, {'countyCode': '002'}))

    def test_valid_county(self):
        self.validator.validate({'countryCode': 'CA', 'stateFipsCode' : '90', 'countyCode': '001'}, {})
        self.assertNotIn('countyCode', self.validator.errors)

    def test_missing_county(self):
        self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90', 'countyCode': '    '}, {})
        self.assertNotIn('countyCode', self.validator.errors)


class CrossFieldRefValidatorForMCDsTestCase(TestCase):

    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.CountryStateReferenceValidator')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.NationalWaterUseCodes')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.SiteTypesCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.LandNetCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.States')
    def setUp(self, mstates_ref, msite_type_ref, mland_net_ref, mwater_use_ref, mref_validator_class):
        ref_list = {
            "countries": [
                {
                    "countryCode": "US",
                    "states": [
                        {
                            "stateFipsCode": "01",
                            "counties": [
                                {
                                    "countyCode": "001",
                                    "minorCivilDivisionCodes": [
                                        "90171",
                                        "90315",
                                        "92106",
                                        "92628"
                                    ]
                                },
                                {
                                    "countyCode": "003",
                                    "minorCivilDivisionCodes": [
                                        "90207",
                                        "90846",
                                        "90963",
                                        "91053",
                                        "91152",
                                        "92754",
                                        "93024",
                                        "93042"
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        mref_validator = mref_validator_class.return_value
        mref_validator.validate.return_value = True
        mref_validator.errors = []

        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefErrorValidator('ref_dir', 'ref_dir')

    def test_mcd_in_list(self):
        self.validator.validate(
            {'countryCode': 'US', 'stateFipsCode': '01', 'countyCode': '001', 'minorCivilDivisionCode': '90171'},
            {}
        )
        self.assertNotIn('minorCivilDivisionCode', self.validator.errors)

    def test_mcd_not_in_list(self):
        self.validator.validate(
            {'countryCode': 'US', 'stateFipsCode': '01', 'countyCode': '001', 'minorCivilDivisionCode': '90172'},
            {}
        )
        self.assertIn('minorCivilDivisionCode', self.validator.errors)

    def test_mcd_null(self):
        self.validator.validate(
            {'countryCode': 'US', 'stateFipsCode': '01', 'countyCode': '001', 'minorCivilDivisionCode': None},
            {}
        )
        self.assertNotIn('minorCivilDivisionCode', self.validator.errors)

    def test_country_state_county_not_in_list(self):
        self.validator.validate(
            {'countryCode': 'CN', 'stateFipsCode': '01', 'countyCode': '001', 'minorCivilDivisionCode': '90172'},
            {}
        )
        self.assertIn('minorCivilDivisionCode', self.validator.errors)

        self.validator.validate(
            {'countryCode': 'US', 'stateFipsCode': '05', 'countyCode': '001', 'minorCivilDivisionCode': '90172'},
            {}
        )
        self.assertIn('minorCivilDivisionCode', self.validator.errors)

        self.validator.validate(
            {'countryCode': 'US', 'stateFipsCode': '01', 'countyCode': '020', 'minorCivilDivisionCode': '90172'},
            {}
        )
        self.assertIn('minorCivilDivisionCode', self.validator.errors)



class CrossFieldRefValidatorForCountiesTestCase(TestCase):
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.CountryStateReferenceValidator')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.NationalWaterUseCodes')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.SiteTypesCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.LandNetCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.States')
    def setUp(self, mstates_ref, msite_type_ref, mland_net_ref, mwater_use_ref, mref_validator_class):
        ref_list = {
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

        mref_validator = mref_validator_class.return_value
        mref_validator.validate.return_value = True
        mref_validator.errors = []

        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefErrorValidator('ref_dir', 'ref_dir')

    def test_county_not_in_list(self):
        self.assertFalse(self.validator.validate({'countryCode': 'CA', 'stateFipsCode' : '90', 'countyCode': '002'}, {}))

        self.assertFalse(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90'}, {'countyCode': '002'}))

    def test_state_not_in_list(self):
        self.assertFalse(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '80', 'countyCode': '002'}, {}))

        self.assertFalse(self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '80'}, {'countyCode': '002'}))

    def test_country_not_in_list(self):
        self.assertFalse(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '80', 'countyCode': '002'}, {}))

        self.assertFalse(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '80'}, {'countyCode': '002'}))

    def test_valid_county(self):
        self.validator.validate({'countryCode': 'CA', 'stateFipsCode' : '90', 'countyCode': '001'}, {})
        self.assertNotIn('countyCode', self.validator.errors)

    def test_missing_county(self):
        self.validator.validate({'countryCode': 'CA', 'stateFipsCode': '90', 'countyCode': '    '}, {})
        self.assertNotIn('countyCode', self.validator.errors)


class CrossFieldRefValidatorForStatesTestCase(TestCase):

    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.CountryStateReferenceValidator')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.NationalWaterUseCodes')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.SiteTypesCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.LandNetCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.Counties')
    def setUp(self, mcounties_ref, msite_type_ref, mland_net_ref, mwater_use_ref, mref_validator_class):
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
        mref_validator = mref_validator_class.return_value
        mref_validator.validate.return_value = True
        mref_validator.errors = []

        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefErrorValidator('ref_dir', 'ref_dir')

    def test_state_not_in_list(self):
        self.assertFalse(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '02'}, {}))
        self.assertEqual(len(self.validator.errors), 1)

        self.assertFalse(self.validator.validate({'countryCode': 'US'}, {'stateFipsCode': '02'}))
        self.assertEqual(len(self.validator.errors), 1)

        self.assertFalse(self.validator.validate({'stateFipsCode': '02'}, {'countryCode': 'US' }))
        self.assertEqual(len(self.validator.errors), 1)

    def test_country_not_in_list(self):
        self.assertTrue(self.validator.validate({'countryCode' : 'CN'}, {'stateFipsCode': '02'}))
        self.assertEqual(len(self.validator.errors), 0)


    def test_state_in_list(self):
        self.assertTrue(self.validator.validate({'countryCode': 'US', 'stateFipsCode': '01'}, {}))
        self.assertEqual(len(self.validator.errors), 0)

        self.assertTrue(self.validator.validate({'countryCode': 'US'}, {'stateFipsCode': '01'}))
        self.assertEqual(len(self.validator.errors), 0)

        self.assertTrue(self.validator.validate({'stateFipsCode': '01'}, {'countryCode': 'US'}))
        self.assertEqual(len(self.validator.errors), 0)

    def test_missing_state(self):
        self.assertTrue(self.validator.validate({'countryCode': 'US'}, {'stateFipsCode' : '  '}))
        self.assertEqual(len(self.validator.errors), 0)

        self.assertTrue(self.validator.validate({}, {'countryCode': 'US'}))
        self.assertEqual(len(self.validator.errors), 0)

    def test_missing_country(self):
        self.assertTrue(self.validator.validate({'stateFipsCode': '01'}, {'countyCode': '   '}))
        self.assertEqual(len(self.validator.errors), 0)

        self.assertTrue(self.validator.validate({}, {'stateFipsCode': '01'}))
        self.assertEqual(len(self.validator.errors), 0)

    def test_valid_latitude_range(self):
        self.assertTrue(self.validator.validate({'latitude': ' 310000'}, {'stateFipsCode': '01', 'countryCode': 'US'}))

    def test_invalid_latitude_range(self):
        self.assertFalse(self.validator.validate({'latitude': ' 500000'}, {'stateFipsCode': '01', 'countryCode': 'US'}))

    def test_missing_fields_latitude_range(self):
        self.assertTrue(self.validator.validate({'latitude': ' 310000'}, {'stateFipsCode': '01'}))
        self.assertTrue(self.validator.validate({'latitude': ' 310000'}, {'countryCode': 'US'}))

    def test_missing_reference_latitude_range(self):
        self.assertTrue(self.validator.validate({'latitude': ' 310000'}, {'stateFipsCode': '01', 'countryCode': 'CN'}))

    def test_valid_longitude_range(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0850000'}, {'stateFipsCode': '01', 'countryCode': 'US'}))

    def test_invalid_longitude_range(self):
        self.assertFalse(self.validator.validate({'longitude': ' 0900000'}, {'stateFipsCode': '01', 'countryCode': 'US'}))

    def test_missing_fields_for_longitude_range(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0850000'}, {'stateFipsCode': '01'}))
        self.assertTrue(self.validator.validate({'longitude': ' 0850000'}, {'countryCode': 'US'}))

    def test_missing_reference_for_longitude_range(self):
        self.assertTrue(self.validator.validate({'longitude': ' 0850000'}, {'stateFipsCode': '01', 'countryCode': 'CN'}))



class CrossFieldRefValidatorForNationalWaterUseTestCase(TestCase):
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.CountryStateReferenceValidator')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.States')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.LandNetCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.SiteTypesCrossField')
    def setUp(self, m_site_type_ref, mland_net_ref, mstates_ref, mref_validator_class):
        ref_list = {
            "siteTypeCodes": [
                {
                    "siteTypeCode": "AG",
                    "nationalWaterUseCodes": ["AQ", "CO"]
                }, {
                    "siteTypeCode": "AS",
                    "nationalWaterUseCodes": ["TE", "WS"]
                }
            ]
        }
        mref_validator = mref_validator_class.return_value
        mref_validator.validate.return_value = True
        mref_validator.errors = []

        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefErrorValidator('ref_dir', 'ref_dir')

    def test_water_use_code_not_in_list(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'AG', 'nationalWaterUseCode': 'CC'}, {}))
        self.assertEqual(len(self.validator.errors), 1)

        self.assertFalse(self.validator.validate({'nationalWaterUseCode': 'CC'}, {'siteTypeCode': 'AG', 'nationalWaterUseCode': 'CO'}))
        self.assertEqual(len(self.validator.errors), 1)

    def test_water_use_code_in_list(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'AG', 'nationalWaterUseCode': 'CO'}, {}))
        self.assertEqual(len(self.validator.errors), 0)

        self.assertTrue(self.validator.validate({'nationalWaterUseCode': 'AQ'},
                                                 {'siteTypeCode': 'AG', 'nationalWaterUseCode': 'CC'}))
        self.assertEqual(len(self.validator.errors), 0)

    def test_missing_fields(self):
       self.assertTrue(self.validator.validate({'siteTypeCode': 'AG'}, {'nationalWaterUseCode': '  '}))
       self.assertEqual(len(self.validator.errors), 0)

       self.assertTrue(self.validator.validate({'nationalWaterUseCode': 'CC'}, {}))
       self.assertEqual(len(self.validator.errors), 0)


class CrossFieldValidatorSiteTypeFieldTestCase(TestCase):
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.CountryStateReferenceValidator')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.States')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.LandNetCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.NationalWaterUseCodes')
    def setUp(self, mwater_use_ref, mland_net_ref, mstates_ref, mref_validator_class):
        ref_list = {
            "siteTypeCodes": [
                {
                    "siteTypeCode": "AG",
                    "notNullAttrs": ['field1'],
                    'nullAttrs': ['field2', 'field3']
                }, {
                    "siteTypeCode": "AS",
                    "notNullAttrs": ['field2', 'field3'],
                    'nullAttrs': ['field1']
                }
            ]
        }
        mref_validator = mref_validator_class.return_value
        mref_validator.validate.return_value = True
        mref_validator.errors = []

        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefErrorValidator('ref_dir', 'ref_dir')

    def test_with_null_attrs_for_site(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'AS', 'field1': '   ', 'field2' : 'A'},
                                                {'field3': 'B'}
                                                ))
        self.assertFalse(self.validator.validate({'siteTypeCode': 'AS', 'field1': 'B', 'field2' : 'A'},
                                                 {'field3': 'B'}
                                                 ))

    def test_with_not_null_attrs_for_site(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'AG', 'field1' : 'A'},
                                                {'field2': '  '}
                                                ))
        self.assertFalse(self.validator.validate({'siteTypeCode': 'AG', 'field1' : '  ' }, {}))

    def test_with_no_reference(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'A', 'field1' : 'A'}, {}))
        self.assertTrue(self.validator.validate({'siteTypeCode': 'A', 'field1': '   '}, {}))


@unittest.skip("not validating land net")
class CrossFieldValidatorLandNetTestCase(TestCase):
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.CountryStateReferenceValidator')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.NationalWaterUseCodes')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.States')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.SiteTypesCrossField')
    @mock.patch('mlrvalidator.validators.cross_field_ref_error_validator.Counties')
    def setUp(self, mcounties_ref, msite_type_ref, mstates_ref, mwater_use_ref, mref_validator_class):
        ref_list = {
                "landNetTemplates": [
                    {
                        "districtCode": "55",
                        "landNetTemplate": "******S???T?????R??????"
                    }
                    ]
                }
        mref_validator = mref_validator_class.return_value
        mref_validator.validate.return_value = True
        mref_validator.errors = []

        with mock.patch('mlrvalidator.validators.reference.open',
                        mock.mock_open(read_data=json.dumps(ref_list))):
            self.validator = CrossFieldRefErrorValidator('ref_dir', 'ref_dir')

    def test_with_existing_district_code_qqqtrs_valid_template(self):
        self.assertTrue(self.validator.validate({'districtCode': '55', 'landNet': 'SWSWSWS010T09832R093425'}, {}))

    def test_with_not_existing_district_code_qqqtrs_valid_template(self):
        self.assertTrue(self.validator.validate({'districtCode': '65', 'landNet': 'SWSWSWS010T09832R093425'}, {}))

    def test_with_existing_district_code_trs_valid_template(self):
        self.assertTrue(self.validator.validate({'districtCode': '55', 'landNet': '      S15 T20N  R11E'}, {}))

    def test_with_existing_district_code_qqqt3r3s2_valid_template(self):
        self.assertTrue(self.validator.validate({'districtCode': '55', 'landNet': 'NWNWSWS15 T014N R022E 4'}, {}))

    def test_with_existing_district_code_qqqt2r2s_valid_template(self):
        self.assertTrue(self.validator.validate({'districtCode': '55', 'landNet': '      S   T23N  R20E  4'}, {}))

    def test_with_existing_district_code_qqqtrs_invalid_char_invalid_template(self):
        self.assertFalse(self.validator.validate({'districtCode': '55', 'landNet': 'NWNWSWS15 T014N R02-E 4'}, {}))

    def test_with_existing_district_code_qqqtrs4_invalid_template(self):
        self.assertFalse(self.validator.validate({'districtCode': '55', 'landNet': 'NWNWSWS15  T014N R022E4'}, {}))

    def test_with_existing_district_code_qqq1trs4_invalid_template(self):
        self.assertFalse(self.validator.validate({'districtCode': '55', 'landNet': 'NWNWSW S15 T014N R022E4'}, {}))

    def test_with_existing_district_code_qqqtrf_invalid_template(self):
        self.assertFalse(self.validator.validate({'districtCode': '55', 'landNet': 'NWNWSWF15 T014N R 022E4'}, {}))

    def test_with_existing_district_code_qqqsrs_invalid_template(self):
        self.assertFalse(self.validator.validate({'districtCode': '55', 'landNet': 'NWNWSWS15 S014N R 022E4'}, {}))

    def test_with_existing_district_code_qqqtss_invalid_template(self):
        self.assertFalse(self.validator.validate({'districtCode': '55', 'landNet': 'NWNWSWF15 T014N S 022E4'}, {}))

    def test_with_existing_district_code_super_wrong_invalid_template(self):
        self.assertFalse(self.validator.validate({'districtCode': '55', 'landNet': 'Q'}, {}))
