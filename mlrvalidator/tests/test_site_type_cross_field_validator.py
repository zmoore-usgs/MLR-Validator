from unittest import TestCase

from mlrvalidator.site_type_cross_field_validator import SiteTypeCrossFieldValidator
from mlrvalidator.schema import site_type_cross_field_schema


class TestValidateSiteTypeCrossFields(TestCase):

    def setUp(self):
        self.validator = SiteTypeCrossFieldValidator(site_type_cross_field_schema)
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

    def test_good_data(self):
        validation_result_1 = self.validator.validate(self.good_data_1)
        validation_result_2 = self.validator.validate(self.good_data_2)
        validation_result_3 = self.validator.validate(self.good_data_3)
        self.assertTrue(validation_result_1)
        self.assertTrue(validation_result_2)
        self.assertTrue(validation_result_3)

    def test_bad_data(self):
        validation_result_1 = self.validator.validate(self.bad_data_1)
        validation_result_2 = self.validator.validate(self.bad_data_2)
        validation_result_3 = self.validator.validate(self.bad_data_3)
        self.assertFalse(validation_result_1)
        self.assertFalse(validation_result_2)
        self.assertFalse(validation_result_3)
