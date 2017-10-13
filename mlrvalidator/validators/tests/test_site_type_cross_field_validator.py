from unittest import TestCase

from ..site_type_cross_field_validator import SiteTypeCrossFieldValidator


class ValidateSiteTypeCrossFieldsTestCase(TestCase):

    def setUp(self):
        self.schema = {'siteTypeCode': {'valid_site_type_cross_field': True}}
        self.validator = SiteTypeCrossFieldValidator(self.schema)
        self.validator.allow_unknown = True
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
        self.bad_data_1 = {'siteTypeCode': 'FA-CI',
                           'longitude': 'F',
                           'latitude': '',
                           'dataReliabilityCode':'j',
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
        validation_result_1 = self.validator.validate(self.good_data_1)
        validation_result_2 = self.validator.validate(self.good_data_2)
        validation_result_3 = self.validator.validate(self.good_data_3)
        validation_result_4 = self.validator.validate(self.good_data_4)
        validation_result_5 = self.validator.validate(self.good_data_5)
        self.assertTrue(validation_result_1)
        self.assertTrue(validation_result_2)
        self.assertTrue(validation_result_3)
        self.assertTrue(validation_result_4)
        self.assertTrue(validation_result_5)

    def test_bad_data(self):
        validation_result_1 = self.validator.validate(self.bad_data_1)
        validation_result_2 = self.validator.validate(self.bad_data_2)
        validation_result_3 = self.validator.validate(self.bad_data_3)
        validation_result_4 = self.validator.validate(self.bad_data_4)
        self.assertFalse(validation_result_1)
        self.assertFalse(validation_result_2)
        self.assertFalse(validation_result_3)
        self.assertFalse(validation_result_4)
