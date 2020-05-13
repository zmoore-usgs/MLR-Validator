
from unittest import TestCase

from app import application
from ..warning_validator import WarningValidator

validator = WarningValidator(application.config['SCHEMA_DIR'], application.config['LOCAL_REFERENCE_DIR'], application.config['REMOTE_REFERENCE_DIR'])


class AltitudeWarningValidationsTestCase(TestCase):
    def test_valid_altitude_range(self):
        validator .validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '1234'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB',
             'countryCode': 'US', 'stateFipsCode': '55'},
            update=True)
        self.assertNotIn('altitude', validator .warnings)

    def test_invalid_altitude_range(self):
        validator .validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '2234'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB',
             'countryCode': 'US', 'stateFipsCode': '55'},
            update=True)
        self.assertIn('altitude', validator .warnings)

    def test_state_not_in_list(self):
        validator .validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '2234'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB',
             'countryCode': 'US', 'stateFipsCode': '80'},
            update=True)
        self.assertNotIn('altitude', validator .warnings)

    def test_country_not_in_list(self):
        validator .validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '2234'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB',
             'countryCode': 'ZZ', 'stateFipsCode': '80'},
            update=True)
        self.assertNotIn('altitude', validator .warnings)

    def test_missing_country_state(self):
        validator .validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '2234'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB',
             'stateFipsCode': '80'},
            update=True)
        self.assertNotIn('altitude', validator .warnings)

        validator .validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '2234'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB',
             'countryCode': 'US'},
            update=True)
        self.assertNotIn('altitude', validator .warnings)


class WarningValidatorStationNameTestCase(TestCase):

    def test_valid_station_name_matching_quotes(self):
        self.assertTrue(validator.validate({'stationName': 'this is a station'}, {}, update=True))

    def test_valid_station_name_spaces_matching_quotes(self):
        self.assertTrue(validator.validate({'stationName': '     '}, {}, update=True))

    def test_valid_station_name_quote_in_middle(self):
        self.assertTrue(validator.validate({'stationName': "This is USGS's Station"}, {}, update=True))

    def test_invalid_quote_at_end(self):
        self.assertFalse(validator.validate({'stationName': "This is a USGS Station'"}, {}, update=True))

    def test_invalid_quote_at_beginning(self):
        self.assertFalse(validator.validate({'stationName': "'This is a USGS Station"}, {}, update=True))


class CountyCodeTestCase(TestCase):

    def test_county_in_latitude_range(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countyCode': '003', 'latitude': ' 460000'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '005'},
            update=True
        )
        self.assertNotIn('latitude', validator.warnings)

    def test_county_not_in_latitude_range(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countyCode': '003', 'latitude': ' 450000'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'countryCode': 'US', 'stateFipsCode': '55',
             'countyCode': '005'},
            update=True
        )
        self.assertIn('latitude', validator.warnings)


class ContributingDrainageAreaTestCase(TestCase):

    def test_contributing_drainage_area_equal_to_drainage_area(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '100'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '100'},
            update=True
        )
        self.assertIn('drainageArea', validator.warnings)

    def test_contributing_drainage_area_not_equal_to_drainage_area(self):
        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '110'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '100'},
            update=True
        )
        self.assertNotIn('drainageArea', validator.warnings)

        validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'contributingDrainageArea': '110'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'drainageArea': '120'},
            update=True
        )
        self.assertNotIn('drainageArea', validator.warnings)

class UseCodesTestCase(TestCase):

    def setUp(self):
        self.site_lists = [['primaryUseOfSiteCode', 'secondaryUseOfSiteCode', 'tertiaryUseOfSiteCode'],
                           ['primaryUseOfWaterCode', 'secondaryUseOfWaterCode', 'tertiaryUseOfWaterCode']]

    def test_unique_use_codes(self):
        for sites in self.site_lists:
            validator.validate(
                {'agencyCode': 'USGS', 'siteNumber': '12345678', sites[0]: 'A'},
                {'agencyCode': 'USGS', 'siteNumber': '12345678', sites[1]: 'B', sites[2]: 'C'},
                update=True
            )
            self.assertNotIn('uniqueUseCodes', validator.warnings)

    def test_non_unique_use_codes(self):
        for sites in self.site_lists:
            validator.validate(
                {'agencyCode': 'USGS', 'siteNumber': '12345678', sites[0]: 'A'},
                {'agencyCode': 'USGS', 'siteNumber': '12345678', sites[1]: 'A', sites[2]: 'A'},
                update=True
            )
            self.assertIn('uniqueUseCodes', validator.warnings)

            validator.validate(
                {'agencyCode': 'USGS', 'siteNumber': '12345678', sites[0]: 'A'},
                {'agencyCode': 'USGS', 'siteNumber': '12345678', sites[1]: 'A', sites[2]: 'C'},
                update=True
            )
            self.assertIn('uniqueUseCodes', validator.warnings)

            validator.validate(
                {'agencyCode': 'USGS', 'siteNumber': '12345678', sites[0]: 'A'},
                {'agencyCode': 'USGS', 'siteNumber': '12345678', sites[1]: 'B', sites[2]: 'A'},
                update=True
            )
            self.assertIn('uniqueUseCodes', validator.warnings)

            validator.validate(
                {'agencyCode': 'USGS', 'siteNumber': '12345678', sites[0]: 'A'},
                {'agencyCode': 'USGS', 'siteNumber': '12345678', sites[1]: 'B', sites[2]: 'B'},
                update=True
            )
            self.assertIn('uniqueUseCodes', validator.warnings)

class WarningValidatorSiteNumberTestCase(TestCase):
    def setUp(self):
        self.v = WarningValidator(application.config['SCHEMA_DIR'], application.config['LOCAL_REFERENCE_DIR'], application.config['REMOTE_REFERENCE_DIR'])

    def test_site_number_wu_no_first_digit_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': 'AW', 'siteNumber': '8765432109'}, {}, update=True))

    def test_site_number_wu_greater_than_max_length_first_digit_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': 'AW', 'siteNumber': '987654321098765432'}, {}, update=True))

    def test_site_number_ll_valid(self):
        self.v.validate({'siteTypeCode': 'AT', 'siteNumber': '012345678901234'}, {}, update=True)
        self.assertNotIn('siteNumber', self.v.warnings)    

    def test_site_number_dsll_min_length_valid(self):
        self.v.validate({'siteTypeCode': 'GL', 'siteNumber': '12345678'}, {}, update=True)
        self.assertNotIn('siteNumber', self.v.warnings)

    def test_site_number_dsll_max_length_valid(self):
        self.v.validate({'siteTypeCode': 'GL', 'siteNumber': '012345678901234'}, {}, update=True)
        self.assertNotIn('siteNumber', self.v.warnings)

    def test_site_number_wu_min_length_first_digit_valid(self):
        self.assertTrue(self.v.validate({'siteTypeCode': 'AW', 'siteNumber': '9876543210'}, {}, update=True))

    def test_site_number_wu_max_length_first_digit_valid(self):
        self.assertTrue(self.v.validate({'siteTypeCode': 'AW', 'siteNumber': '987654321098765'}, {}, update=True))

    def test_site_number_llwu_max_length_first_digit_valid(self):
        self.v.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '987654321098765'}, {}, update=True)
        self.assertNotIn('siteNumber', self.v.warnings)

    def test_site_number_llwu_max_length_valid(self):
        self.v.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '087654321098765'}, {}, update=True)
        self.assertNotIn('siteNumber', self.v.warnings)

    def test_site_number_llwu_min_length_valid(self):
        self.v.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '9876543210'}, {}, update=True)
        self.assertNotIn('siteNumber', self.v.warnings)

    def test_site_number_ll_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': 'AT', 'siteNumber': '01234567890123'}, {}, update=True))

    def test_site_number_dsll_less_than_min_length_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': 'GL', 'siteNumber': '1234567'}, {}, update=True))

    def test_site_number_dsll_greater_than_max_length_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': 'GL', 'siteNumber': '0123456789012345'}, {}, update=True))

    def test_site_number_wu_less_than_min_length_first_digit_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': 'AW', 'siteNumber': '987654321'}, {}, update=True))

    def test_site_number_llwu_greater_than_max_length_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '98765432109876543'}, {}, update=True))

    def test_site_number_llwu_less_than_min_length_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '59876543'}, {}, update=True))

    def test_site_number_llwu_wrong_first_digit_invalid(self):
        self.assertFalse(self.v.validate({'siteTypeCode': 'FA-CI', 'siteNumber': '087654321098'}, {}, update=True))