
from unittest import TestCase
from mlrvalidator.reference import Aquifers, Hucs, Mcds, NationalAquifers, NationalWaterUseCodes, Counties, \
    States, SiteTypes, SiteTypesCrossField


class ValidateGetAquifersCase(TestCase):
    def setUp(self):
        self.aquifer = Aquifers('references/aquifer.json')

    def test_validate_ok(self):
        good_aquifer = ["112EVRS", "112GLCV", "112SUMS"]
        test_aquifer = self.aquifer.get_aquifers('CA', '96')

        self.assertEqual(test_aquifer, good_aquifer)

    def test_validate_not_ok(self):
        bad_aquifer = []
        test_aquifer = self.aquifer.get_aquifers('CA', '01')

        self.assertEqual(test_aquifer, bad_aquifer)

        bad_aquifer = []
        test_aquifer = self.aquifer.get_aquifers('XY', '96')

        self.assertEqual(test_aquifer, bad_aquifer)


class ValidateGetNationalAquifersCase(TestCase):
    def setUp(self):
        self.national_aquifer = NationalAquifers('references/national_aquifer.json')

    def test_validate_ok(self):
        good_aquifer = ["N100AKUNCD", "N9999OTHER"]
        test_aquifer = self.national_aquifer.get_national_aquifers('US', '02')

        self.assertEqual(test_aquifer, good_aquifer)

    def test_validate_not_ok(self):
        bad_aquifer = []
        test_aquifer = self.national_aquifer.get_national_aquifers('US', 'XY')

        self.assertEqual(test_aquifer, bad_aquifer)

        bad_aquifer = []
        test_aquifer = self.national_aquifer.get_national_aquifers('XY', '01')

        self.assertEqual(test_aquifer, bad_aquifer)


class ValidateGetHucsCase(TestCase):
    def setUp(self):
        self.huc = Hucs('references/huc.json')

    def test_validate_ok(self):
        good_huc = ["21030001"]
        test_huc = self.huc.get_hucs('PM', '61')

        self.assertEqual(test_huc, good_huc)

    def test_validate_not_ok(self):
        bad_huc = []
        test_huc = self.huc.get_hucs('PM', 'XY')

        self.assertEqual(test_huc, bad_huc)

        bad_huc = []
        test_huc = self.huc.get_hucs('XY', '61')

        self.assertEqual(test_huc, bad_huc)


class ValidateGetMcdsCase(TestCase):
    def setUp(self):
        self.mcd = Mcds('references/mcd.json')

    def test_validate_ok(self):
        good_mcd = ["90148",
            "90296",
            "90444",
            "90740",
            "90888",
            "91036",
            "91110",
            "91332",
            "91480",
            "91628",
            "91776",
            "91924",
            "92072",
            "92220",
            "92368",
            "92516",
            "92664",
            "92738",
            "92812",
            "92960",
            "93108",
            "93256",
            "93404",
            "93552",
            "93700",
            "93848",
            "93996"]
        test_mcd = self.mcd.get_mcds('US', '10')

        self.assertEqual(test_mcd, good_mcd)

    def test_validate_not_ok(self):
        bad_mcd = []
        test_mcd = self.mcd.get_mcds('US', 'XY')

        self.assertEqual(test_mcd, bad_mcd)

        bad_mcd = []
        test_mcd = self.mcd.get_mcds('XY', '10')

        self.assertEqual(test_mcd, bad_mcd)


class ValidateGetNationalWaterUseCase(TestCase):
    def setUp(self):
        self.national_water_use = NationalWaterUseCodes('references/national_water_use.json')

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
        self.county = Counties('references/county.json')

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
        self.county = Counties('references/county.json')

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
        self.state = States('references/state.json')

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
        self.state = States('references/state.json')

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


class ValidateGetSiteTypesCase(TestCase):
    def setUp(self):
        self.site_type = SiteTypes('references/site_type_transition.json')

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
        test_new_site_type = self.site_type.get_site_types('AG')

        self.assertEqual(test_new_site_type, good_new_site_type)

    def test_validate_not_ok(self):
        bad_new_site_type = []
        test_new_site_type = self.site_type.get_site_types('XY')

        self.assertEqual(test_new_site_type, bad_new_site_type)


class ValidateGetSiteTypesCrossFieldCase(TestCase):

    def setUp(self):
        self.site_type_cf = SiteTypesCrossField('references/site_type_cross_field.json')

    def test_real_site_type_code(self):
        result = self.site_type_cf.get_site_type_field_dependencies('SB-CV')
        expected = {'notNullableAttrs': ['longitude',
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
        with self.assertRaises(StopIteration):
            self.site_type_cf.get_site_type_field_dependencies('Obi-Wan Kenobi')
