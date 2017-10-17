
from unittest import TestCase

from ..error_validator import ErrorValidator

class ErrorValidatorLatitudeTestCase(TestCase):
    #TODO: fill in with additional tests for latitude. Ideally each field that has validations would have a separate test case.

    def latitude_without_longitude_is_invalid(self):
        self.assertFalse(self.validator.validate({'latitude': ' 0400000'}, {}))

class ValidateCrossFieldsTestCase(TestCase):

    #TODO: Break this up so that a test case tests a fields validation rules. Below is the cross field validation schema tests
    #TODO: Add needed tests for all validations not just cross field.
    #TODO: Add tests with an existing document
    def setUp(self):
        self.validator = ErrorValidator()
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


class SiteTypeCrossFieldValidationWithSchema(TestCase):
    #TODO: Break this up so that a field's validation tests are in a single test case
    #TODO: Add tests with an existing document

    def setUp(self):
        self.validator = ErrorValidator()
        self.good_data_1 = {'siteTypeCode': 'FA-CS',
                            'dataReliabilityCode': 'x',
                            'aquiferTypeCode': '',
                            'aquiferCode': '',
                            'contributingDrainageArea': '',
                            'nationalWaterUseCode': '',
                            'drainageArea': '',
                            'nationalAquiferCode': ''
                            }
        self.good_data_2 = {'siteTypeCode': 'ES',
                            'longitude': 'O',
                            'latitude': 'j',
                            'dataReliabilityCode': 'E',
                            'aquiferTypeCode': '',
                            'secondaryUseOfSite': '',
                            'aquiferCode': '',
                            'wellDepth': '',
                            'sourceOfDepthCode': '',
                            'nationalAquiferCode': '',
                            'tertiaryUseOfSiteCode': '',
                            'holeDepth': ''
                            }
        self.good_data_3 = {'siteTypeCode': 'ST-CA',
                            'longitude': 'R',
                            'latitude': 'D',
                            'dataReliabilityCode': 'm',
                            'secondaryUseOfSite': '',
                            'tertiaryUseOfSiteCode': ''
                            }
        self.good_data_4 = {'siteTypeCode': ' ',
                            'dataReliabilityCode': 'x',
                            'aquiferTypeCode': '',
                            'aquiferCode': '',
                            'contributingDrainageArea': '',
                            'nationalWaterUseCode': '',
                            'drainageArea': '',
                            'nationalAquiferCode': '    '
                            }
        # tests that this is still good data if a required null field is absent
        # absent fields are commented out
        self.good_data_5 = {'siteTypeCode': 'FA-DV',
                            'longitude': 'p',
                            'latitude': 'B',
                            'dataReliabilityCode': 'z',
                            'aquiferTypeCode': '',
                            'aquiferCode': '',
                            # 'contributingDrainageArea': '',
                            # 'nationalWaterUseCode': '',
                            'drainageArea': '',
                            'nationalAquiferCode': ''
                            }
        # test neutral data (i.e. a totally wrong site type code)
        # validations of site type code value are out of scope for the site type cross field validator
        self.neutral_data = {'siteTypeCode': 'Darth Vader',
                             'longitude': 'F',
                             'latitude': '',
                             'dataReliabilityCode': 'j',
                             'aquiferTypeCode': '',
                             'aquiferCode': '',
                             'contributingDrainageArea': '',
                             'nationalWaterUseCode': '',
                             'drainageArea': '',
                             'nationalAquiferCode': ''
                             }
        self.bad_data_1 = {'siteTypeCode': 'FA-CI',
                           'longitude': 'F',
                           'latitude': '',
                           'dataReliabilityCode': 'j',
                           'aquiferTypeCode': '',
                           'aquiferCode': '',
                           'contributingDrainageArea': '',
                           'nationalWaterUseCode': '',
                           'drainageArea': '',
                           'nationalAquiferCode': ''
                           }
        self.bad_data_2 = {'siteTypeCode': 'GW-HZ',
                           'longitude': 'f',
                           'latitude': 'W',
                           'primaryUseOfSite': 'b',
                           'dataReliabilityCode': 'F',
                           'aquiferTypeCode': '',
                           'aquiferCode': '',
                           'contributingDrainageArea': '',
                           'wellDepth': '',
                           'nationalWaterUseCode': '',
                           'sourceOfDepthCode': '',
                           'drainageArea': 'J',
                           'nationalAquiferCode': '',
                           'holeDepth': 'K'
                           }
        self.bad_data_3 = {'siteTypeCode': 'FA-WIW',
                           'longitude': '',
                           'latitude': 'f',
                           'dataReliabilityCode': 'w',
                           'aquiferTypeCode': '',
                           'aquiferCode': '',
                           'contributingDrainageArea': 'C',
                           'wellDepth': '',
                           'nationalWaterUseCode': '',
                           'sourceOfDepthCode': '',
                           'drainageArea': 'N',
                           'nationalAquiferCode': '',
                           'holeDepth': ''
                           }
        # test that this is bad data if a required field is absent
        # absent fields are commented out
        self.bad_data_4 = {'siteTypeCode': 'SB-GWD',
                           'longitude': 'Z',
                           'latitude': 'F',
                           # 'primaryUseOfSite': 'W',
                           'dataReliabilityCode': 'F',
                           'aquiferTypeCode': '',
                           'aquiferCode': '',
                           'contributingDrainageArea': '',
                           'wellDepth': '',
                           'nationalWaterUseCode': '',
                           'sourceOfDepthCode': '',
                           'drainageArea': '',
                           'nationalAquiferCode': '',
                           'holeDepth': ''
                           }

    def test_good_data(self):
        validation_result_1 = self.validator.validate(self.good_data_1, {}, update=True)
        validation_result_2 = self.validator.validate(self.good_data_2, {}, update=True)
        validation_result_3 = self.validator.validate(self.good_data_3, {}, update=True)
        validation_result_4 = self.validator.validate(self.good_data_4, {}, update=True)
        validation_result_5 = self.validator.validate(self.good_data_5, {}, update=True)
        self.assertTrue(validation_result_1)
        self.assertTrue(validation_result_2)
        self.assertTrue(validation_result_3)
        self.assertTrue(validation_result_4)
        self.assertTrue(validation_result_5)

    def test_neutral_data(self):
        validation_result = self.validator.validate(self.neutral_data, {}, update=True)
        self.assertTrue(validation_result)

    def test_bad_data(self):
        validation_result_1 = self.validator.validate(self.bad_data_1,{}, update=True)
        validation_result_2 = self.validator.validate(self.bad_data_2, {}, update=True)
        validation_result_3 = self.validator.validate(self.bad_data_3, {}, update=True)
        validation_result_4 = self.validator.validate(self.bad_data_4, {}, update=True)
        self.assertFalse(validation_result_1)
        self.assertFalse(validation_result_2)
        self.assertFalse(validation_result_3)
        self.assertFalse(validation_result_4)