
from unittest import TestCase

from app import application
from ..error_validator import ErrorValidator


class ValidateCrossFieldsTestCase(TestCase):

    #TODO: Break this up so that a test case tests a fields validation rules. Below is the cross field validation schema tests
    #TODO: Add needed tests for all validations not just cross field.
    #TODO: Add tests with an existing document
    def setUp(self):
        self.validator = ErrorValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])
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
            'altitudeMethodCode': 'A',
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
            'secondaryUseOfSite': '',
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
            'secondaryUseOfWaterCode': '',
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
        self.assertTrue(self.validator.validate(self.good_data, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data2, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data3, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data4, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data5, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data6, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data7, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data8, {}, update=True))
        self.assertTrue(self.validator.validate(self.good_data9, {}, update=True))
        #TODO: Fix validate_type_numeric to return true for empty strings and strings with all blanks.
        #self.validator.validate(self.good_data10, {}, update=True)
        #self.assertTrue(self.validator.validate(self.good_data11, {}, update=True))
        #self.assertTrue(self.validator.validate(self.good_data12, {}, update=True))


    def test_validate_not_ok(self):
        self.assertFalse(self.validator.validate(self.bad_data, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data2, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data3, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data4, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data5, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data6, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data7, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data8, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data9, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data10, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data11, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data12, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data13, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data14, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data15, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data16, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data17, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data18, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data19, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data20, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data21, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data22, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data23, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data24, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data25, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data26, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data27, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data28, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data29, {}, update=True))
        self.assertFalse(self.validator.validate(self.bad_data30, {}, update=True))


class AltitudeErrorValidationsTestCase(TestCase):

    def setUp(self):
        self.validator = ErrorValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])

    def test_optional(self):
        self.validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': ' '}, {},)
        self.assertNotIn('altitude', self.validator.errors)

        self.validator.validate({'agencyCode': 'USGS ', 'siteNumber': '12345678'}, {})
        self.assertNotIn('altitude', self.validator.errors)

    def test_reciprocal_dependency(self):
        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345',  'altitudeAccuracyValue' : 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitude', self.validator.errors)

        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeAccuracyValue': ' '},
            {'altitude': '12345',  'altitudeAccuracyValue' : 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertIn('altitude', self.validator.errors)

        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeMethodCode': ' '},
            {'altitude': '12345', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertIn('altitude', self.validator.errors)

        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitudeDatumCode': ' '},
            {'altitude': '12345', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertIn('altitude', self.validator.errors)


    def test_max_length(self):
        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345', 'altitudeAccuracyValue' : 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678'}, update=True)
        self.assertNotIn('altitude', self.validator.errors)

        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '123456789', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'},
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', }, update=True)
        self.assertIn('altitude', self.validator.errors)

    def test_numeric(self):
        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertNotIn('altitude', self.validator.errors)

        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-12345'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'}, update=True)
        self.assertNotIn('altitude', self.validator.errors)

        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345.1'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertNotIn('altitude', self.validator.errors)

        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-12A'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertIn('altitude', self.validator.errors)

    def test_two_decimal_precison(self):
        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345.23'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertNotIn('altitude', self.validator.errors)

        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '12345.233'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertIn('altitude', self.validator.errors)

        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-1234.23'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertNotIn('altitude', self.validator.errors)

        self.validator.validate(
            {'agencyCode': 'USGS ', 'siteNumber': '12345678', 'altitude': '-1234.233'},
            {'altitude': '1234', 'altitudeAccuracyValue': 'A', 'altitudeMethodCode': 'AAA', 'altitudeDatumCode': 'BBB'},
            update=True)
        self.assertIn('altitude', self.validator.errors)


class AltitudeWarningValidationsTestCase(TestCase):
    def setUp(self):
        self.validator = WarnValidator(application.config['SCHEMA_DIR'], application.config['REFERENCE_FILE_DIR'])










