from unittest import TestCase
from mlrvalidator.site_file_cross_field_validator_rules import CrossFieldValidator
from mlrvalidator.schema import cross_field_schema

cross_field_validator = CrossFieldValidator(cross_field_schema)
cross_field_validator.allow_unknown = True

class ValidateCrossFields(TestCase):

    def setUp(self):
        self.good_data = {
            'latitude': ' 123456',
            'longitude': ' 1234556',
            'coordinateAccuracyCode': '1',
            'coordinateDatumCode': 'ABIDJAN',
            'coordinateMethodCode': 'C'
        }
        self.good_data2 = {
            'altitude': '1234',
            'altitudeDatumCode': 'ASVD02',
            'altitudeAccuracyValue': '12'
        }
        self.good_data3 = {
            'primaryUseOfSite': 'A',
            'secondaryUseOfSite': 'C',
            'tertiaryUseOfSiteCode': 'E'
        }
        self.good_data4 = {
            'primaryUseOfWaterCode': 'A',
            'secondaryUseOfWaterCode': 'C',
            'tertiaryUseOfWaterCode': 'E'
        }
        self.good_data5 = {
            'firstConstructionDate': '20000101',
            'siteEstablishmentDate': '20000102'
        }
        self.good_data6 = {
            'firstConstructionDate': '200001',
            'siteEstablishmentDate': '200101'
        }
        self.good_data7 = {
            'firstConstructionDate': '2000',
            'siteEstablishmentDate': '2001'
        }
        self.good_data8 = {
            'wellDepth': '10',
            'holeDepth': '10'
        }
        self.good_data9 = {
            'wellDepth': '10',
            'holeDepth': '11'
        }
        self.good_data10 = {
            'wellDepth': '',
            'holeDepth': '10'
        }
        self.good_data11 = {
            'wellDepth': '10',
            'holeDepth': ''
        }
        self.good_data12 = {
            'wellDepth': '',
            'holeDepth': ''
        }
        self.bad_data = {
            'latitude': '',
            'longitude': '',
            'coordinateAccuracyCode': '1',
            'coordinateDatumCode': 'ABIDJAN',
            'coordinateMethodCode': 'C'
        }
        self.bad_data2 = {
            'latitude': ' 123456',
            'longitude': '',
        }
        self.bad_data3 = {
            'latitude': '',
            'longitude': ' 1234556',
        }
        self.bad_data4 = {
            'latitude': ' 123456',
            'longitude': ' 1234556',
            'coordinateAccuracyCode': '',
            'coordinateDatumCode': 'ABIDJAN',
            'coordinateMethodCode': 'C'
        }
        self.bad_data5 = {
            'latitude': ' 123456',
            'longitude': ' 1234556',
            'coordinateAccuracyCode': '1',
            'coordinateDatumCode': '',
            'coordinateMethodCode': 'C'
        }
        self.bad_data6 = {
            'latitude': ' 123456',
            'longitude': ' 1234556',
            'coordinateAccuracyCode': '1',
            'coordinateDatumCode': 'ABIDJAN',
            'coordinateMethodCode': ''
        }
        self.bad_data7 = {
            'latitude': ' 123456',
            'longitude': ' 1234556',
            'coordinateAccuracyCode': '',
            'coordinateDatumCode': '',
            'coordinateMethodCode': ''
        }
        self.bad_data8 = {
            'altitude': '',
            'altitudeDatumCode': 'ASVD02',
            'altitudeAccuracyValue': '12',
            'altitudeMethodCode': 'A'
        }
        self.bad_data9 = {
            'altitude': '1234',
            'altitudeDatumCode': '',
            'altitudeAccuracyValue': '12',
            'altitudeMethodCode': 'A'
        }
        self.bad_data10 = {
            'altitude': '1234',
            'altitudeDatumCode': 'ASVD02',
            'altitudeAccuracyValue': '',
            'altitudeMethodCode': 'A'
        }
        self.bad_data11 = {
            'altitude': '1234',
            'altitudeDatumCode': 'ASVD02',
            'altitudeAccuracyValue': '12',
            'altitudeMethodCode': ''
        }
        self.bad_data12 = {
            'altitude': '1234',
            'altitudeDatumCode': '',
            'altitudeAccuracyValue': '',
            'altitudeMethodCode': ''
        }
        self.bad_data13 = {
            'primaryUseOfSite': 'A',
            'secondaryUseOfSite': 'A',
            'tertiaryUseOfSiteCode': 'A'
        }
        self.bad_data14 = {
            'primaryUseOfSite': 'A',
            'secondaryUseOfSite': 'A',
            'tertiaryUseOfSiteCode': 'C'
        }
        self.bad_data15 = {
            'primaryUseOfSite': 'A',
            'secondaryUseOfSite': 'C',
            'tertiaryUseOfSiteCode': 'A'
        }
        self.bad_data16 = {
            'primaryUseOfSite': 'C',
            'secondaryUseOfSite': 'A',
            'tertiaryUseOfSiteCode': 'A'
        }
        self.bad_data17 = {
            'primaryUseOfSite': '',
            'secondaryUseOfSite': 'C',
            'tertiaryUseOfSiteCode': 'E'
        }
        self.bad_data18 = {
            'primaryUseOfSite': 'A',
            'secondaryUseOfSite': '',
            'tertiaryUseOfSiteCode': 'E'
        }
        self.bad_data19 = {
            'primaryUseOfSite': '',
            'secondaryUseOfSite': 'C',
            'tertiaryUseOfSiteCode': 'E'
        }
        self.bad_data20 = {
            'primaryUseOfWaterCode': 'A',
            'secondaryUseOfWaterCode': 'A',
            'tertiaryUseOfWaterCode': 'A'
        }
        self.bad_data21 = {
            'primaryUseOfWaterCode': 'A',
            'secondaryUseOfWaterCode': 'A',
            'tertiaryUseOfWaterCode': 'C'
        }
        self.bad_data22 = {
            'primaryUseOfWaterCode': 'A',
            'secondaryUseOfWaterCode': 'C',
            'tertiaryUseOfWaterCode': 'A'
        }
        self.bad_data23 = {
            'primaryUseOfWaterCode': 'C',
            'secondaryUseOfWaterCode': 'A',
            'tertiaryUseOfWaterCode': 'A'
        }
        self.bad_data24 = {
            'primaryUseOfWaterCode': '',
            'secondaryUseOfWaterCode': 'C',
            'tertiaryUseOfWaterCode': 'E'
        }
        self.bad_data25 = {
            'primaryUseOfWaterCode': 'A',
            'secondaryUseOfWaterCode': '',
            'tertiaryUseOfWaterCode': 'E'
        }
        self.bad_data26 = {
            'primaryUseOfWaterCode': '',
            'secondaryUseOfWaterCode': 'C',
            'tertiaryUseOfWaterCode': 'E'
        }
        self.bad_data27 = {
            'firstConstructionDate': '20000102',
            'siteEstablishmentDate': '20000101'
        }
        self.bad_data28 = {
            'firstConstructionDate': '200002',
            'siteEstablishmentDate': '200001'
        }
        self.bad_data29 = {
            'firstConstructionDate': '2001',
            'siteEstablishmentDate': '2000'
        }
        self.bad_data30 = {
            'wellDepth': '11',
            'holeDepth': '10'
        }

    def test_validate_ok(self):
        self.assertTrue(cross_field_validator.validate(self.good_data))
        self.assertTrue(cross_field_validator.validate(self.good_data2))
        self.assertTrue(cross_field_validator.validate(self.good_data3))
        self.assertTrue(cross_field_validator.validate(self.good_data4))
        self.assertTrue(cross_field_validator.validate(self.good_data5))
        self.assertTrue(cross_field_validator.validate(self.good_data6))
        self.assertTrue(cross_field_validator.validate(self.good_data7))
        self.assertTrue(cross_field_validator.validate(self.good_data8))
        self.assertTrue(cross_field_validator.validate(self.good_data9))
        self.assertTrue(cross_field_validator.validate(self.good_data10))
        self.assertTrue(cross_field_validator.validate(self.good_data11))
        self.assertTrue(cross_field_validator.validate(self.good_data12))


    def test_validate_not_ok(self):
        self.assertFalse(cross_field_validator.validate(self.bad_data))
        self.assertFalse(cross_field_validator.validate(self.bad_data2))
        self.assertFalse(cross_field_validator.validate(self.bad_data3))
        self.assertFalse(cross_field_validator.validate(self.bad_data4))
        self.assertFalse(cross_field_validator.validate(self.bad_data5))
        self.assertFalse(cross_field_validator.validate(self.bad_data6))
        self.assertFalse(cross_field_validator.validate(self.bad_data7))
        self.assertFalse(cross_field_validator.validate(self.bad_data8))
        self.assertFalse(cross_field_validator.validate(self.bad_data9))
        self.assertFalse(cross_field_validator.validate(self.bad_data10))
        self.assertFalse(cross_field_validator.validate(self.bad_data11))
        self.assertFalse(cross_field_validator.validate(self.bad_data12))
        self.assertFalse(cross_field_validator.validate(self.bad_data13))
        self.assertFalse(cross_field_validator.validate(self.bad_data14))
        self.assertFalse(cross_field_validator.validate(self.bad_data15))
        self.assertFalse(cross_field_validator.validate(self.bad_data16))
        self.assertFalse(cross_field_validator.validate(self.bad_data17))
        self.assertFalse(cross_field_validator.validate(self.bad_data18))
        self.assertFalse(cross_field_validator.validate(self.bad_data19))
        self.assertFalse(cross_field_validator.validate(self.bad_data20))
        self.assertFalse(cross_field_validator.validate(self.bad_data21))
        self.assertFalse(cross_field_validator.validate(self.bad_data22))
        self.assertFalse(cross_field_validator.validate(self.bad_data23))
        self.assertFalse(cross_field_validator.validate(self.bad_data24))
        self.assertFalse(cross_field_validator.validate(self.bad_data25))
        self.assertFalse(cross_field_validator.validate(self.bad_data26))
        self.assertFalse(cross_field_validator.validate(self.bad_data27))
        self.assertFalse(cross_field_validator.validate(self.bad_data28))
        self.assertFalse(cross_field_validator.validate(self.bad_data29))
        self.assertFalse(cross_field_validator.validate(self.bad_data30))



