
from unittest import TestCase
from mlrvalidator.reference import get_aquifers, get_national_aquifers, get_hucs, get_mcds, \
    get_national_water_use_codes, get_counties, get_county_attributes


class ValidateGetAquifersCase(TestCase):

    def test_validate_ok(self):
        good_aquifer = ["112EVRS", "112GLCV", "112SUMS"]
        test_aquifer = get_aquifers('CA', '96')

        self.assertEqual(test_aquifer, good_aquifer)

    def test_validate_not_ok(self):
        bad_aquifer = []
        test_aquifer = get_aquifers('CA', '01')

        self.assertEqual(test_aquifer, bad_aquifer)

        bad_aquifer = []
        test_aquifer = get_aquifers('XY', '96')

        self.assertEqual(test_aquifer, bad_aquifer)


class ValidateGetNationalAquifersCase(TestCase):

    def test_validate_ok(self):
        good_aquifer = ["N100AKUNCD", "N9999OTHER"]
        test_aquifer = get_national_aquifers('US', '02')

        self.assertEqual(test_aquifer, good_aquifer)

    def test_validate_not_ok(self):
        bad_aquifer = []
        test_aquifer = get_national_aquifers('US', 'XY')

        self.assertEqual(test_aquifer, bad_aquifer)

        bad_aquifer = []
        test_aquifer = get_national_aquifers('XY', '01')

        self.assertEqual(test_aquifer, bad_aquifer)


class ValidateGetHucsCase(TestCase):

    def test_validate_ok(self):
        good_huc = ["21030001"]
        test_huc = get_hucs('PM', '61')

        self.assertEqual(test_huc, good_huc)

    def test_validate_not_ok(self):
        bad_huc = []
        test_huc = get_hucs('PM', 'XY')

        self.assertEqual(test_huc, bad_huc)

        bad_huc = []
        test_huc = get_hucs('XY', '61')

        self.assertEqual(test_huc, bad_huc)


class ValidateGetMcdsCase(TestCase):

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
        test_mcd = get_mcds('US', '10')

        self.assertEqual(test_mcd, good_mcd)

    def test_validate_not_ok(self):
        bad_mcd = []
        test_mcd = get_mcds('US', 'XY')

        self.assertEqual(test_mcd, bad_mcd)

        bad_mcd = []
        test_mcd = get_mcds('XY', '10')

        self.assertEqual(test_mcd, bad_mcd)


class ValidateGetNationalWaterUseCase(TestCase):

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
        test_national_water_use = get_national_water_use_codes('AS')

        self.assertEqual(test_national_water_use, good_national_water_use)

    def test_validate_not_ok(self):
        bad_national_water_use = []
        test_national_water_use = get_national_water_use_codes('XY')

        self.assertEqual(test_national_water_use, bad_national_water_use)


class ValidateGetCountiesCase(TestCase):

    def test_validate_ok(self):
        good_county = ["000", "005", "040", "050", "060"]
        test_county = get_counties('FM', '64')

        self.assertEqual(test_county, good_county)

    def test_validate_not_ok(self):
        bad_county = []
        test_county = get_counties('FM', 'XY')

        self.assertEqual(test_county, bad_county)

        bad_county = []
        test_county = get_counties('XY', '64')

        self.assertEqual(test_county, bad_county)


class ValidateGetCountyCase(TestCase):

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
        test_county = get_county_attributes('FM', '64', '000')

        self.assertEqual(test_county, good_county)

    def test_validate_not_ok(self):
        bad_county = {}
        test_county = get_county_attributes('FM', '64', '999')

        self.assertEqual(test_county, bad_county)

        bad_county = {}
        test_county = get_county_attributes('XY', '64', '000')

        self.assertEqual(test_county, bad_county)

        bad_county = {}
        test_county = get_county_attributes('FM', 'XY', '000')

        self.assertEqual(test_county, bad_county)