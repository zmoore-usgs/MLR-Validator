
import json
from unittest import TestCase, mock

from ..location_validator import Location_Validator
from .. reference import SiteTypesCrossField

class LocationValidatorTestCase(TestCase):

    def setUp(self):
        ref_list = {
            "siteTypeCodes": [
                {
                    "notNullAttrs": ["longitude","latitude"],
                    "nullAttrs": [],
                    "siteTypeCode": "SB-CV"
                },{
                    "notNullAttrs" : [],
                    "nullAttrs": ["latitude", "longitude"],
                    "siteTypeCode": "SB-UZ"
                }
            ]
        }

        with mock.patch('mlrvalidator.validators.reference.open', mock.mock_open(read_data=json.dumps(ref_list))):
            site_type_ref = SiteTypesCrossField('fake_file')

        self.validator = Location_Validator(site_type_ref)

    def test_bad_reciprocal_dependency(self):
        self.assertFalse(self.validator.validate({'latitude': ' 0400000'}, {}))
        self.assertIsNotNone(self.validator.errors)

        self.assertFalse(self.validator.validate({'latitude': ' 0400000', 'longitude': ' 1000000'},
                                                 {'coordinateAccuracyCode': '1234', 'coordinateDatumCode': '   '}))
        self.assertIsNotNone(self.validator.errors)

        self.assertFalse(self.validator.validate({'latitude': ' 0400000', 'longitude': ' 1000000'},
                                                 {'coordinateAccuracyCode': ' ', 'coordinateDatumCode': '12', 'coordinateMethodCode': ' '}))
        self.assertIsNotNone(self.validator.errors)

    def test_null_location_when_site_type_requires_location(self):
        self.assertFalse(self.validator.validate({'siteTypeCode' : 'SB-CV'}, {'siteTypeCode': 'BB'}))
        self.assertIsNotNone(self.validator.errors)

        self.assertFalse(self.validator.validate({'latitude': '   ', 'longitude': ' ', 'coordinateAccuracyCode': ' ', 'coordinateDatumCode': ' ', 'coordinateMethodCode' : ' '},
                                                 {'siteTypeCode': 'SB-CV', 'latitude': ' 0400000', 'longitude': ' 1000000', 'coordinateAccuracyCode': 'AA', 'coordinateDatumCode': '12', 'coordinateMethodCode': 'D'}))
        self.assertIsNotNone(self.validator.errors)

    def test_location_when_site_type_does_not_allow_location(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'SB-UZ'}, {'latitude': ' 0400000', 'longitude': ' 1000000', 'coordinateAccuracyCode': 'AA', 'coordinateDatumCode': '12', 'coordinateMethodCode': 'D', }))
        self.assertIsNotNone(self.validator.errors)

    def test_valid_location(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'SB-CV'},
                                                 {'latitude': ' 0400000', 'longitude': ' 1000000',
                                                  'coordinateAccuracyCode': 'AA', 'coordinateDatumCode': '12',
                                                  'coordinateMethodCode': 'D', }))
        self.assertIsNone(self.validator.errors)

        self.assertTrue(self.validator.validate({'siteTypeCode': 'SB'},
                                                {'latitude': ' 0400000', 'longitude': ' 1000000',
                                                 'coordinateAccuracyCode': 'AA', 'coordinateDatumCode': '12',
                                                 'coordinateMethodCode': 'D', }))
        self.assertIsNone(self.validator.errors)

        self.assertTrue(self.validator.validate(
            {'latitude': '   ', 'longitude': ' ', 'coordinateAccuracyCode': ' ', 'coordinateDatumCode': ' ',
             'coordinateMethodCode': ' ', 'siteTypeCode' : 'SB-UZ'}, {}))
        self.assertIsNone(self.validator.errors)

        self.assertTrue(self.validator.validate(
            {'latitude': '   ', 'longitude': ' ', 'coordinateAccuracyCode': ' ', 'coordinateDatumCode': ' ',
             'coordinateMethodCode': ' ', 'siteTypeCode': 'SB'}, {}))
        self.assertIsNone(self.validator.errors)

