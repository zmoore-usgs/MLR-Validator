
from unittest import TestCase

from app import application
from ..warning_validator import WarningValidator

validator = WarningValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])


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

