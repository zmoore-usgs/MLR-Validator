
import json
from unittest import TestCase, mock

from ..transition_validator import TransitionValidator

class TransitionValidatorSiteTypeTestCase(TestCase):

    @mock.patch('mlrvalidator.validators.transition_validator.SiteTypeInvalidCodes')
    @mock.patch('mlrvalidator.validators.transition_validator.FieldTransitions')
    def setUp(self, mfield_transitions, msite_type_invalid_codes):
    
        msite_type_invalid_codes.return_value.get_site_type_invalid_codes.return_value = ['FA', 'SS']
        mfield_transitions.return_value.get_allowed_transitions.return_value = ['FA-SPS', 'FA-WIW', 'FA-DV', 'FA-OF']
        self.validator = TransitionValidator('ref_dir')

    def test_valid_transition(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-DV'}, {'siteTypeCode': 'AS'}))

    def test_invalid_transition(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'SP'}, {'siteTypeCode': 'AS'}))

    def test_missing_field(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-DV'}, {}))
    
    def test_missing_field2(self):
        self.assertTrue(self.validator.validate({}, {'siteTypeCode': 'AG'}))

    def test_existing_not_in_ref_list(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'FA-DV'}, {'siteTypeCode': 'AB'}))

    def test_no_change_from_existing_to_new(self):
        self.assertTrue(self.validator.validate({'siteTypeCode': 'AG'}, {'siteTypeCode': 'AG'}))

    def test_invalid_site_type_transition(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'FA'}, {'siteTypeCode': 'FA'}))
    
    def test_invalid_site_type_transition2(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'SS'}, {'siteTypeCode': 'SS'}))
        
    def test_invalid_site_type_transition3(self):
        self.assertFalse(self.validator.validate({}, {'siteTypeCode': 'SS'}))

    def test_valid_existing_site_type_not_updated(self):
        self.assertTrue(self.validator.validate({}, {'siteNumber': '410421095581902','agencyCode': 'USGS ', 'primaryUseOfSiteCode': 'W', 'dataReliabilityCode': 'C'}))

    def test_valid_existing_site_type_not_updated2(self):
        self.assertTrue(self.validator.validate({}, {'siteNumber': '422927088151601','agencyCode': 'USGS ', 'remarks': 'Test Remark for 422927088151601 2/4/2019'}))

    def test_valid_existing_site_type_not_updated3(self):
        self.assertTrue(self.validator.validate({}, {'databaseTableIdentifier': '0','transactionType': 'M','stationName': 'test 342323091232356                              ','siteTypeCode': 'GW','districtCode': '05','countryCode': 'US','stateFipsCode': '05','countyCode': '001','latitude': ' 342323','longitude': ' 0912323','coordinateAccuracyCode': 'U','coordinateMethodCode': 'U','coordinateDatumCode': 'NAD83','timeZoneCode': 'CST','daylightSavingsTimeFlag': 'Y','nationalWaterUseCode': 'IR','siteWebReadyCode': 'Y','dataReliabilityCode': 'C','primaryUseOfSiteCode': 'W','agencyCode': 'USGS ','siteNumber': '342323091232356'}))

class TransitionValidatorSiteTypeTestCase2(TestCase):

    @mock.patch('mlrvalidator.validators.transition_validator.SiteTypeInvalidCodes')
    @mock.patch('mlrvalidator.validators.transition_validator.FieldTransitions')
    def setUp(self, mfield_transitions, msite_type_invalid_codes):
    
        msite_type_invalid_codes.return_value.get_site_type_invalid_codes.return_value = ['FA', 'SS']
        mfield_transitions.return_value.get_allowed_transitions.return_value = ['FA-SPS','FA-WIW','GW']
        self.validator = TransitionValidator('ref_dir')

    def test_valid_transition(self):
        self.assertFalse(self.validator.validate({'siteTypeCode': 'FA-DV'}, {'siteTypeCode': 'AG'}))
