import json
import os
from unittest import TestCase, mock

from app import application
from ..reference import CountryStateReference, NationalWaterUseCodes, States, FieldTransitions, SiteTypesCrossField, Counties


class CountryStateReferenceTestCase(TestCase):
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
            self.aquifer_ref = CountryStateReference('fake_file', 'aquiferCodes')

    def test_list_that_exists(self):
        self.assertEqual(self.aquifer_ref.get_list_by_country_state('US', '02'), ['000MCRL', '000SELS'])

    def test_missing_country(self):
        self.assertEqual(self.aquifer_ref.get_list_by_country_state('CN', '02'), [])

    def test_missing_state(self):
        self.assertEqual(self.aquifer_ref.get_list_by_country_state('US', '03'), [])


class ValidateGetNationalWaterUseCase(TestCase):
    def setUp(self):
        self.national_water_use = NationalWaterUseCodes(os.path.join(application.config['REFERENCE_FILE_DIR'], 'national_water_use.json'))

    def test_validate_ok(self):
        good_national_water_use = [
            "AQ",
            "CO",
            "DO",
            "IN",
            "IR",
            "LV",
            "MI",
            "RM",
            "ST",
            "TE",
            "WS"
        ]
        test_national_water_use = self.national_water_use.get_national_water_use_codes('AS')

        self.assertEqual(test_national_water_use, good_national_water_use)

    def test_validate_not_ok(self):
        bad_national_water_use = []
        test_national_water_use = self.national_water_use.get_national_water_use_codes('XY')

        self.assertEqual(test_national_water_use, bad_national_water_use)


class ValidateGetCountyCodeCase(TestCase):
    def setUp(self):
        self.county = Counties(os.path.join(application.config['REFERENCE_FILE_DIR'], 'county.json'), 'counties')

    def test_validate_ok(self):
        good_county = ["000", "005", "040", "050", "060"]
        test_county = self.county.get_county_codes('FM', '64')

        self.assertEqual(test_county, good_county)

    def test_validate_not_ok(self):
        bad_county = []
        test_county = self.county.get_county_codes('FM', 'XY')

        self.assertEqual(test_county, bad_county)

        bad_county = []
        test_county = self.county.get_county_codes('XY', '64')

        self.assertEqual(test_county, bad_county)


class ValidateGetCountyAttributesCase(TestCase):
    def setUp(self):
        self.county = Counties(os.path.join(application.config['REFERENCE_FILE_DIR'], 'county.json'), 'counties')

    def test_validate_ok(self):
        good_county = {
              "countyCode": "000",
              "county_min_lat_va": "010400",
              "county_max_lat_va": "100700",
              "county_min_long_va": "-1630200",
              "county_max_long_va": "-1380000",
              "county_min_alt_va": "00000",
              "county_max_alt_va": "02600"
            }
        test_county = self.county.get_county_attributes('FM', '64', '000')

        self.assertEqual(test_county, good_county)

    def test_validate_not_ok(self):
        bad_county = {}
        test_county = self.county.get_county_attributes('FM', '64', '999')

        self.assertEqual(test_county, bad_county)

        bad_county = {}
        test_county = self.county.get_county_attributes('XY', '64', '000')

        self.assertEqual(test_county, bad_county)

        bad_county = {}
        test_county = self.county.get_county_attributes('FM', 'XY', '000')

        self.assertEqual(test_county, bad_county)


class ValidateGetStateCodeCase(TestCase):
    def setUp(self):
        self.state = States(os.path.join(application.config['REFERENCE_FILE_DIR'], 'state.json'))

    def test_validate_ok(self):
        good_state = ["00", "90", "91", "92", "93", "94", "95", "96", "97", "98"]
        test_state = self.state.get_state_codes('CA')

        self.assertEqual(test_state, good_state)

    def test_validate_not_ok(self):
        bad_state = []
        test_state = self.state.get_state_codes('XY')

        self.assertEqual(test_state, bad_state)


class ValidateGetStateAttributesCase(TestCase):
    def setUp(self):
        self.state = States(os.path.join(application.config['REFERENCE_FILE_DIR'], 'state.json'))

    def test_validate_ok(self):
        good_state = {
          "stateFipsCode": "00",
          "state_min_lat_va": "414036",
          "state_max_lat_va": "694000",
          "state_min_long_va": "0553000",
          "state_max_long_va": "1410000",
          "state_min_alt_va": "00000",
          "state_max_alt_va": "30000"
        }
        test_state = self.state.get_state_attributes('CA', '00')

        self.assertEqual(test_state, good_state)

    def test_validate_not_ok(self):
        bad_state = {}
        test_state = self.state.get_state_attributes('CA', 'XY')

        self.assertEqual(test_state, bad_state)

        bad_state = {}
        test_state = self.state.get_state_attributes('XY', '00')

        self.assertEqual(test_state, bad_state)

class ValidateGetFieldTransitionsCase(TestCase):
    def setUp(self):
        self.site_type = FieldTransitions(os.path.join(application.config['REFERENCE_FILE_DIR'], 'site_type_transition.json'))

    def test_validate_ok(self):
        good_new_site_type = [
            "FA-SPS",
            "FA-WIW",
            "GW",
            "GW-CR",
            "GW-IW",
            "GW-MW",
            "SP"
        ]
        test_new_site_type = self.site_type.get_allowed_transitions('AG')

        self.assertEqual(test_new_site_type, good_new_site_type)


    def test_validate_not_ok(self):
        bad_new_site_type = []
        test_new_site_type = self.site_type.get_allowed_transitions('XY')

        self.assertEqual(test_new_site_type, bad_new_site_type)


class ValidateGetSiteTypesCrossFieldCase(TestCase):

    def setUp(self):
        self.site_type_cf = SiteTypesCrossField(os.path.join(application.config['REFERENCE_FILE_DIR'], 'site_type_cross_field.json'))

    def test_real_site_type_code(self):
        result = self.site_type_cf.get_site_type_field_dependencies('SB-CV')
        expected = {'notNullAttrs': ['longitude',
                                     'latitude',
                                     'primaryUseOfSite',
                                     'dataReliabilityCode'
                                     ],
                    'nullAttrs': ['aquiferTypeCode',
                                  'aquiferCode',
                                  'contributingDrainageArea',
                                  'wellDepth',
                                  'sourceOfDepthCode',
                                  'drainageArea',
                                  'nationalAquiferCode',
                                  'holeDepth'
                                  ],
                    'siteTypeCode': 'SB-CV'
                    }
        self.assertEqual(result, expected)

    def test_site_type_code_with_padding(self):
        result = self.site_type_cf.get_site_type_field_dependencies('   SB-CV  ')
        expected = {'notNullAttrs': ['longitude',
                                     'latitude',
                                     'primaryUseOfSite',
                                     'dataReliabilityCode'
                                     ],
                    'nullAttrs': ['aquiferTypeCode',
                                  'aquiferCode',
                                  'contributingDrainageArea',
                                  'wellDepth',
                                  'sourceOfDepthCode',
                                  'drainageArea',
                                  'nationalAquiferCode',
                                  'holeDepth'
                                  ],
                    'siteTypeCode': 'SB-CV'
                    }
        self.assertEqual(result, expected)

    def test_non_existent_site_type_code(self):
        site_type_cd = 'Obi-Wan Kenobi'
        result = self.site_type_cf.get_site_type_field_dependencies('Obi-Wan Kenobi')
        expected = {'siteTypeCode': site_type_cd, 'notNullAttrs': [], 'nullAttrs': []}
        self.assertEqual(result, expected)
