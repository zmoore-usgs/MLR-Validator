
from unittest import TestCase

from app import application
from ..warning_validator import WarningValidator

validator = WarningValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])


class AltitudeWarningValidationsTestCase(TestCase):
    def setUp(self):
        validator = WarningValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])

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