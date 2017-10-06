
from unittest import TestCase
from mlrvalidator.site_file_validator_warnings import SitefileWarningValidator
from mlrvalidator.schema import warning_schema

site_validator = SitefileWarningValidator(warning_schema)
site_validator.allow_unknown = True


class ValidateWarningsCase(TestCase):
    def setUp(self):
        self.good_data = {
            'stationName': '12345'
        }
        self.bad_data = {
            'stationName': "12345'"
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_data))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_data))


class ValidateValidCountyRange(TestCase):

    def setUp(self):
        self.good_not_us_country = {
            'countryCode': 'UP',
            'stateFipsCode': '00',
            'countyCode': '000',
            'latitude': '9999999',
            'longitude': '9999999'
        }
        self.good_no_attributes = {
            'countryCode': 'US',
            'stateFipsCode': '76',
            'countyCode': '000',
            'latitude': '9999999',
            'longitude': '9999999'
        }
        self.good_min_lat_min_long = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '300840',
            'longitude': '0845318'
        }
        self.good_max_lat_max_long = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '350029',
            'longitude': '0882824'
        }
        self.good_mid_lat_mid_long = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '330840',
            'longitude': '0865318'
        }
        self.good_min_lat_min_long_edges = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '300840.001',
            'longitude': '0845318.001'
        }
        self.good_max_lat_max_long_edges = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '350028.999',
            'longitude': '0882823.999'
        }
        self.bad_min_lat_min_long = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '300140',
            'longitude': '0815318'
        }
        self.bad_min_lat_good_min_long = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '300140',
            'longitude': '0845318'
        }
        self.bad_max_lat_good_max_long = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '380029',
            'longitude': '0882824'
        }
        self.good_min_lat_bad_min_long = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '300840',
            'longitude': '0815318'
        }
        self.good_max_lat_bad_max_long = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '350029',
            'longitude': '0982824'
        }
        self.bad_max_lat_max_long = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '380029',
            'longitude': '0982824'
        }
        self.bad_min_lat_min_long_edges = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '300139.999',
            'longitude': '0815317.999'
        }
        self.bad_max_lat_max_long_edges = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'countyCode': '000',
            'latitude': '380029.001',
            'longitude': '0982824.001'
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_not_us_country))
        self.assertTrue(site_validator.validate(self.good_no_attributes))
        self.assertTrue(site_validator.validate(self.good_min_lat_min_long))
        self.assertTrue(site_validator.validate(self.good_max_lat_max_long))
        self.assertTrue(site_validator.validate(self.good_mid_lat_mid_long))
        self.assertTrue(site_validator.validate(self.good_min_lat_min_long_edges))
        self.assertTrue(site_validator.validate(self.good_max_lat_max_long_edges))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_min_lat_min_long))
        self.assertFalse(site_validator.validate(self.bad_max_lat_max_long))
        self.assertFalse(site_validator.validate(self.bad_min_lat_min_long_edges))
        self.assertFalse(site_validator.validate(self.bad_max_lat_max_long_edges))
        self.assertFalse(site_validator.validate(self.bad_min_lat_good_min_long))
        self.assertFalse(site_validator.validate(self.bad_max_lat_good_max_long))
        self.assertFalse(site_validator.validate(self.good_min_lat_bad_min_long))
        self.assertFalse(site_validator.validate(self.good_max_lat_bad_max_long))


class ValidateValidStateRange(TestCase):

    def setUp(self):
        self.good_not_us_country = {
            'countryCode': 'AF',
            'stateFipsCode': '00',
            'latitude': '9999999',
            'longitude': '9999999'
        }
        self.good_no_attributes = {
            'countryCode': 'US',
            'stateFipsCode': '76',
            'latitude': '9999999',
            'longitude': '9999999'
        }
        self.good_min_lat_min_long = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '365933',
            'longitude': '1020227'
        }
        self.good_max_lat_max_long = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '410012',
            'longitude': '1090337'
        }
        self.good_mid_lat_mid_long = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '385933',
            'longitude': '1070227'
        }
        self.good_min_lat_min_long_edges = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '365933.001',
            'longitude': '1020227.001'
        }
        self.good_max_lat_max_long_edges = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '410011.999',
            'longitude': '1090336.999'
        }
        self.good_min_lat_min_long_negs = {
            'countryCode': 'US',
            'stateFipsCode': '77',
            'latitude': '053000',
            'longitude': '-1270000'
        }
        self.good_max_lat_max_long_negs = {
            'countryCode': 'US',
            'stateFipsCode': '77',
            'latitude': '190000',
            'longitude': '-1170000'
        }
        self.good_mid_lat_mid_long_negs = {
            'countryCode': 'US',
            'stateFipsCode': '77',
            'latitude': '153000',
            'longitude': '-1220000'
        }
        self.bad_min_lat_min_long = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '305933',
            'longitude': '1000227'
        }
        self.bad_min_lat_min_long_negs = {
            'countryCode': 'US',
            'stateFipsCode': '77',
            'latitude': '003000',
            'longitude': '-1470000'
        }
        self.bad_min_lat_good_long = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '305933',
            'longitude': '1070227'
        }
        self.bad_max_lat_good_long = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '420012',
            'longitude': '1070227'
        }
        self.bad_max_lat_max_long = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '420012',
            'longitude': '1090337'
        }
        self.bad_max_lat_max_long_negs = {
            'countryCode': 'US',
            'stateFipsCode': '77',
            'latitude': '290000',
            'longitude': '-1070000'
        }
        self.bad_max_long_good_lat = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '385933',
            'longitude': '1100337'
        }
        self.bad_min_long_good_lat = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '385933',
            'longitude': '1000227'
        }
        self.bad_min_lat_min_long_edges = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '365932.999',
            'longitude': '1020226.999'
        }
        self.bad_max_lat_max_long_edges = {
            'countryCode': 'US',
            'stateFipsCode': '08',
            'latitude': '410012.001',
            'longitude': '1090337.001'
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_not_us_country))
        self.assertTrue(site_validator.validate(self.good_no_attributes))
        self.assertTrue(site_validator.validate(self.good_min_lat_min_long))
        self.assertTrue(site_validator.validate(self.good_max_lat_max_long))
        self.assertTrue(site_validator.validate(self.good_mid_lat_mid_long))
        self.assertTrue(site_validator.validate(self.good_min_lat_min_long_edges))
        self.assertTrue(site_validator.validate(self.good_max_lat_max_long_edges))
        self.assertTrue(site_validator.validate(self.good_min_lat_min_long_negs))
        self.assertTrue(site_validator.validate(self.good_max_lat_max_long_negs))
        self.assertTrue(site_validator.validate(self.good_mid_lat_mid_long_negs))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_min_lat_min_long))
        self.assertFalse(site_validator.validate(self.bad_min_lat_min_long_negs))
        self.assertFalse(site_validator.validate(self.bad_min_lat_good_long))
        self.assertFalse(site_validator.validate(self.bad_max_lat_good_long))
        self.assertFalse(site_validator.validate(self.bad_max_lat_max_long))
        self.assertFalse(site_validator.validate(self.bad_max_lat_max_long_negs))
        self.assertFalse(site_validator.validate(self.bad_max_long_good_lat))
        self.assertFalse(site_validator.validate(self.bad_min_long_good_lat))
        self.assertFalse(site_validator.validate(self.bad_min_lat_min_long_edges))
        self.assertFalse(site_validator.validate(self.bad_max_lat_max_long_edges))


class ValidateValidAltitudeRange(TestCase):

    def setUp(self):
        self.good_no_attributes = {
            'countryCode': 'RM',
            'stateFipsCode': '00',
            'altitude': '999'
        }
        self.good_goofy_ranges = {
            'countryCode': 'US',
            'stateFipsCode': '37',
            'altitude': '300',
            'latitude': '334510',
            'longitude': '0752400'
        }
        self.good_null_altitude = {
            'countryCode': 'US',
            'stateFipsCode': '37',
            'altitude': '',
            'latitude': '334510',
            'longitude': '0752400'
        }
        self.good_space_altitude = {
            'countryCode': 'US',
            'stateFipsCode': '37',
            'altitude': ' ',
            'latitude': '334510',
            'longitude': '0752400'
        }
        self.good_min_altitude = {
            'countryCode': 'US',
            'stateFipsCode': '42',
            'altitude': '0',
            'latitude': '394311',
            'longitude': '0744122'
        }
        self.good_min_neg_altitude = {
            'countryCode': 'US',
            'stateFipsCode': '48',
            'altitude': '-10',
            'latitude': '255014',
            'longitude': '0933029'
        }
        self.good_max_altitude = {
            'countryCode': 'US',
            'stateFipsCode': '42',
            'altitude': '3213',
            'latitude': '394311',
            'longitude': '0744122'
        }
        self.good_mid_altitude = {
            'countryCode': 'US',
            'stateFipsCode': '42',
            'altitude': '999',
            'latitude': '394311',
            'longitude': '0744122'
        }
        self.good_decimal_altitude = {
            'countryCode': 'US',
            'stateFipsCode': '42',
            'altitude': '99.26',
            'latitude': '394311',
            'longitude': '0744122'
        }
        self.bad_min_altitude = {
            'countryCode': 'US',
            'stateFipsCode': '42',
            'altitude': '-9',
            'latitude': '394311',
            'longitude': '0744122'
        }
        self.bad_min_neg_altitude = {
            'countryCode': 'US',
            'stateFipsCode': '48',
            'altitude': '-16',
            'latitude': '255014',
            'longitude': '0933029'
        }
        self.bad_max_altitude = {
            'countryCode': 'US',
            'stateFipsCode': '42',
            'altitude': '13213',
            'latitude': '394311',
            'longitude': '0744122'
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_no_attributes))
        self.assertTrue(site_validator.validate(self.good_goofy_ranges))
        self.assertTrue(site_validator.validate(self.good_null_altitude))
        self.assertTrue(site_validator.validate(self.good_space_altitude))
        self.assertTrue(site_validator.validate(self.good_min_altitude))
        self.assertTrue(site_validator.validate(self.good_min_neg_altitude))
        self.assertTrue(site_validator.validate(self.good_max_altitude))
        self.assertTrue(site_validator.validate(self.good_mid_altitude))
        self.assertTrue(site_validator.validate(self.good_decimal_altitude))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_min_altitude))
        self.assertFalse(site_validator.validate(self.bad_min_neg_altitude))
        self.assertFalse(site_validator.validate(self.bad_max_altitude))
