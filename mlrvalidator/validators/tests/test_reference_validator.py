
from unittest import TestCase
from ..reference_validator import ReferenceValidator
from mlrvalidator.schema import reference_schema

site_validator = ReferenceValidator(reference_schema)
site_validator.allow_unknown = True


class ValidateReferenceCase(TestCase):

    def setUp(self):
        self.good_data = {
            'agencyCode': 'USGS'
        }
        self.good_data2 = {
            'agencyCode': 'USGS '
        }
        self.good_data3 = {
            'agencyUseCode': 'A'
        }
        self.good_data4 = {
            'altitudeDatumCode': 'LMSL'
        }
        self.good_data5 = {
            'altitudeMethodCode': 'A'
        }
        self.good_data6 = {
            'altitudeMethodCode': ' '
        }
        self.good_data7 = {
            'altitudeMethodCode': ''
        }
        self.good_data8 = {
            'aquiferTypeCode': 'C'
        }
        self.good_data9 = {
            'coordinateDatumCode': 'ACCRA'
        }
        self.good_data10 = {
            'coordinateMethodCode': 'C'
        }
        self.good_data11 = {
            'coordinateAccuracyCode': '1'
        }
        self.good_data12 = {
            'coordinateAccuracyCode': ' '
        }
        self.good_data13 = {
            'coordinateAccuracyCode': ''
        }
        self.good_data14 = {
            'countryCode': 'US'
        }
        self.good_data15 = {
            'dataReliabilityCode': 'C'
        }
        self.good_data16 = {
            'districtCode': '01'
        }
        self.good_data17 = {
            'primaryUseOfSite': 'A'
        }
        self.good_data18 = {
            'primaryUseOfWaterCode': 'A'
        }
        self.good_data19 = {
            'secondaryUseOfSite': 'A'
        }
        self.good_data20 = {
            'secondaryUseOfWaterCode': 'A'
        }
        self.good_data21 = {
            'siteTypeCode': 'AG'
        }
        self.good_data22 = {
            'siteWebReadyCode': 'C'
        }
        self.good_data23 = {
            'tertiaryUseOfSiteCode': 'A'
        }
        self.good_data24 = {
            'tertiaryUseOfWaterCode': 'A'
        }
        self.good_data25 = {
            'timeZoneCode': 'CST'
        }
        self.good_data26 = {
            'topographicCode': 'A'
        }
        self.good_data27 = {
            'topographicCode': 'a'
        }
        self.good_data28 = {
            'sourceOfDepthCode': 'a'
        }
        self.good_data29 = {
            'sourceOfDepthCode': 'A'
        }
        self.bad_data = {
            'agencyCode': 'x'
        }
        self.bad_data2 = {
            'agencyUseCode': 'XYZ'
        }
        self.bad_data3 = {
            'altitudeDatumCode': 'XYZ'
        }
        self.bad_data4 = {
            'altitudeMethodCode': 'B'
        }
        self.bad_data5 = {
            'aquiferTypeCode': 'B'
        }
        self.bad_data6 = {
            'coordinateDatumCode': 'XYZ'
        }
        self.bad_data7 = {
            'coordinateMethodCode': 'A'
        }
        self.bad_data8 = {
            'coordinateAccuracyCode': 'A'
        }
        self.bad_data9 = {
            'countryCode': 'XY'
        }
        self.bad_data10 = {
            'dataReliabilityCode': 'A'
        }
        self.bad_data11 = {
            'districtCode': '99'
        }
        self.bad_data12 = {
            'primaryUseOfSite': 'B'
        }
        self.bad_data13 = {
            'primaryUseOfWaterCode': 'V'
        }
        self.bad_data14 = {
            'secondaryUseOfSite': 'B'
        }
        self.bad_data15 = {
            'secondaryUseOfWaterCode': 'V'
        }
        self.bad_data16 = {
            'siteTypeCode': 'AA'
        }
        self.bad_data17 = {
            'siteWebReadyCode': 'F'
        }
        self.bad_data18 = {
            'tertiaryUseOfSiteCode': 'B'
        }
        self.bad_data19 = {
            'tertiaryUseOfWaterCode': 'V'
        }
        self.bad_data20 = {
            'timeZoneCode': 'XYZ'
        }
        self.bad_data21 = {
            'topographicCode': 'I'
        }
        self.bad_data22 = {
            'sourceOfDepthCode': 'X'
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_data))
        self.assertTrue(site_validator.validate(self.good_data2))
        self.assertTrue(site_validator.validate(self.good_data3))
        self.assertTrue(site_validator.validate(self.good_data4))
        self.assertTrue(site_validator.validate(self.good_data5))
        self.assertTrue(site_validator.validate(self.good_data6))
        self.assertTrue(site_validator.validate(self.good_data7))
        self.assertTrue(site_validator.validate(self.good_data8))
        self.assertTrue(site_validator.validate(self.good_data9))
        self.assertTrue(site_validator.validate(self.good_data10))
        self.assertTrue(site_validator.validate(self.good_data11))
        self.assertTrue(site_validator.validate(self.good_data12))
        self.assertTrue(site_validator.validate(self.good_data13))
        self.assertTrue(site_validator.validate(self.good_data14))
        self.assertTrue(site_validator.validate(self.good_data15))
        self.assertTrue(site_validator.validate(self.good_data16))
        self.assertTrue(site_validator.validate(self.good_data17))
        self.assertTrue(site_validator.validate(self.good_data18))
        self.assertTrue(site_validator.validate(self.good_data19))
        self.assertTrue(site_validator.validate(self.good_data20))
        self.assertTrue(site_validator.validate(self.good_data21))
        self.assertTrue(site_validator.validate(self.good_data22))
        self.assertTrue(site_validator.validate(self.good_data23))
        self.assertTrue(site_validator.validate(self.good_data24))
        self.assertTrue(site_validator.validate(self.good_data25))
        self.assertTrue(site_validator.validate(self.good_data26))
        self.assertTrue(site_validator.validate(self.good_data27))
        self.assertTrue(site_validator.validate(self.good_data28))
        self.assertTrue(site_validator.validate(self.good_data29))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_data))
        self.assertFalse(site_validator.validate(self.bad_data2))
        self.assertFalse(site_validator.validate(self.bad_data3))
        self.assertFalse(site_validator.validate(self.bad_data4))
        self.assertFalse(site_validator.validate(self.bad_data5))
        self.assertFalse(site_validator.validate(self.bad_data6))
        self.assertFalse(site_validator.validate(self.bad_data7))
        self.assertFalse(site_validator.validate(self.bad_data8))
        self.assertFalse(site_validator.validate(self.bad_data9))
        self.assertFalse(site_validator.validate(self.bad_data10))
        self.assertFalse(site_validator.validate(self.bad_data11))
        self.assertFalse(site_validator.validate(self.bad_data12))
        self.assertFalse(site_validator.validate(self.bad_data13))
        self.assertFalse(site_validator.validate(self.bad_data14))
        self.assertFalse(site_validator.validate(self.bad_data15))
        self.assertFalse(site_validator.validate(self.bad_data16))
        self.assertFalse(site_validator.validate(self.bad_data17))
        self.assertFalse(site_validator.validate(self.bad_data18))
        self.assertFalse(site_validator.validate(self.bad_data19))
        self.assertFalse(site_validator.validate(self.bad_data20))
        self.assertFalse(site_validator.validate(self.bad_data21))
        self.assertFalse(site_validator.validate(self.bad_data22))


class ValidateAquiferCode(TestCase):

    def setUp(self):
        self.good_data = {
            'countryCode': 'CA',
            'stateFipsCode': '96',
            'aquiferCode': '112EVRS'
        }
        self.good_data2 = {
            'countryCode': 'CA',
            'stateFipsCode': '96',
            'aquiferCode': ' '
        }
        self.good_data3 = {
            'countryCode': 'CA',
            'stateFipsCode': '96',
            'aquiferCode': ''
        }
        self.good_data4 = {
            'countryCode': 'ca',
            'stateFipsCode': '96',
            'aquiferCode': '112EVRS'
        }
        self.good_data5 = {
            'countryCode': 'CA',
            'stateFipsCode': '96',
            'aquiferCode': '112evrs'
        }
        self.bad_data = {
            'countryCode': 'CA',
            'stateFipsCode': '96',
            'aquiferCode': '112EVS'
        }
        self.bad_data2 = {
            'countryCode': 'XY',
            'stateFipsCode': '96',
            'aquiferCode': '112EVRS'
        }
        self.bad_data3 = {
            'countryCode': 'CA',
            'stateFipsCode': 'XY',
            'aquiferCode': '112EVRS'
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_data))
        self.assertTrue(site_validator.validate(self.good_data2))
        self.assertTrue(site_validator.validate(self.good_data3))
        self.assertTrue(site_validator.validate(self.good_data4))
        self.assertTrue(site_validator.validate(self.good_data5))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_data))
        self.assertFalse(site_validator.validate(self.bad_data2))
        self.assertFalse(site_validator.validate(self.bad_data3))


class ValidateNationalAquiferCode(TestCase):

    def setUp(self):
        self.good_data = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'nationalAquiferCode': 'S100MSEMBM'
        }
        self.good_data2 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'nationalAquiferCode': ' '
        }
        self.good_data3 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'nationalAquiferCode': ''
        }
        self.good_data4 = {
            'countryCode': 'us',
            'stateFipsCode': '01',
            'nationalAquiferCode': 'S100MSEMBM'
        }
        self.good_data5 = {
            'countryCode': 'us',
            'stateFipsCode': '01',
            'nationalAquiferCode': 's100msembm'
        }
        self.bad_data = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'nationalAquiferCode': 'S100MSMBM'
        }
        self.bad_data2 = {
            'countryCode': 'XY',
            'stateFipsCode': '96',
            'nationalAquiferCode': 'S100MSEMBM'
        }
        self.bad_data3 = {
            'countryCode': 'CA',
            'stateFipsCode': 'XY',
            'nationalAquiferCode': 'S100MSEMBM'
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_data))
        self.assertTrue(site_validator.validate(self.good_data2))
        self.assertTrue(site_validator.validate(self.good_data3))
        self.assertTrue(site_validator.validate(self.good_data4))
        self.assertTrue(site_validator.validate(self.good_data5))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_data))
        self.assertFalse(site_validator.validate(self.bad_data2))
        self.assertFalse(site_validator.validate(self.bad_data3))


class ValidateHydrologicUnitCode(TestCase):

    def setUp(self):
        self.good_data = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'hydrologicUnitCode': '03'
        }
        self.good_data2 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'hydrologicUnitCode': '0313'
        }
        self.good_data3 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'hydrologicUnitCode': '031300'
        }
        self.good_data4 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'hydrologicUnitCode': '03130002'
        }
        self.good_data5 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'hydrologicUnitCode': '0313000206'
        }
        self.good_data6 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'hydrologicUnitCode': '031300020601'
        }
        self.good_data7 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'hydrologicUnitCode': ' '
        }
        self.good_data8 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'hydrologicUnitCode': ''
        }
        self.good_data9 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'hydrologicUnitCode': '99999999'
        }
        self.good_data10 = {
            'countryCode': 'us',
            'stateFipsCode': '01',
            'hydrologicUnitCode': '03'
        }
        self.bad_data = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'hydrologicUnitCode': 'xyz'
        }
        self.bad_data2 = {
            'countryCode': 'XY',
            'stateFipsCode': '01',
            'hydrologicUnitCode': '031300020601'
        }
        self.bad_data3 = {
            'countryCode': 'US',
            'stateFipsCode': 'XY',
            'hydrologicUnitCode': '031300020601'
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_data))
        self.assertTrue(site_validator.validate(self.good_data2))
        self.assertTrue(site_validator.validate(self.good_data3))
        self.assertTrue(site_validator.validate(self.good_data4))
        self.assertTrue(site_validator.validate(self.good_data5))
        self.assertTrue(site_validator.validate(self.good_data6))
        self.assertTrue(site_validator.validate(self.good_data7))
        self.assertTrue(site_validator.validate(self.good_data8))
        self.assertTrue(site_validator.validate(self.good_data9))
        self.assertTrue(site_validator.validate(self.good_data10))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_data))
        self.assertFalse(site_validator.validate(self.bad_data2))
        self.assertFalse(site_validator.validate(self.bad_data3))


class ValidateMinorCivilDivisionCode(TestCase):

    def setUp(self):
        self.good_data = {
            'countryCode': 'US',
            'stateFipsCode': '10',
            'minorCivilDivisionCode': '92664'
        }
        self.good_data2 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'minorCivilDivisionCode': ' '
        }
        self.good_data3 = {
            'countryCode': 'US',
            'stateFipsCode': '01',
            'minorCivilDivisionCode': ''
        }
        self.good_data4 = {
            'countryCode': 'us',
            'stateFipsCode': '10',
            'minorCivilDivisionCode': '92664'
        }
        self.bad_data = {
            'countryCode': 'US',
            'stateFipsCode': '10',
            'minorCivilDivisionCode': '00000'
        }
        self.bad_data2 = {
            'countryCode': 'XY',
            'stateFipsCode': '10',
            'minorCivilDivisionCode': '92664'
        }
        self.bad_data3 = {
            'countryCode': 'US',
            'stateFipsCode': 'XY',
            'minorCivilDivisionCode': '92664'
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_data))
        self.assertTrue(site_validator.validate(self.good_data2))
        self.assertTrue(site_validator.validate(self.good_data3))
        self.assertTrue(site_validator.validate(self.good_data4))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_data))
        self.assertFalse(site_validator.validate(self.bad_data2))
        self.assertFalse(site_validator.validate(self.bad_data3))


class ValidateNationalWaterUseCode(TestCase):

    def setUp(self):
        self.good_data = {
            'siteTypeCode': 'AS',
            'nationalWaterUseCode': 'AQ'
        }
        self.good_data2 = {
            'siteTypeCode': 'AS',
            'nationalWaterUseCode': ' '
        }
        self.good_data3 = {
            'siteTypeCode': 'AS',
            'nationalWaterUseCode': ''
        }
        self.good_data4 = {
            'siteTypeCode': 'as',
            'nationalWaterUseCode': 'aq'
        }
        self.bad_data = {
            'siteTypeCode': 'XY',
            'nationalWaterUseCode': 'AQ'
        }
        self.bad_data2 = {
            'siteTypeCode': 'AS',
            'nationalWaterUseCode': 'XY'
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_data))
        self.assertTrue(site_validator.validate(self.good_data2))
        self.assertTrue(site_validator.validate(self.good_data3))
        self.assertTrue(site_validator.validate(self.good_data4))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_data))
        self.assertFalse(site_validator.validate(self.bad_data2))


class ValidateCountyCode(TestCase):

    def setUp(self):
        self.good_data = {
            'countryCode': 'FM',
            'stateFipsCode': '64',
            'countyCode': '050'
        }
        self.good_data2 = {
            'countryCode': 'FM',
            'stateFipsCode': '64',
            'countyCode': ' '
        }
        self.good_data3 = {
            'countryCode': 'FM',
            'stateFipsCode': '64',
            'countyCode': ''
        }
        self.good_data4 = {
            'countryCode': 'fm',
            'stateFipsCode': '64',
            'countyCode': '050'
        }
        self.bad_data = {
            'countryCode': 'FM',
            'stateFipsCode': '64',
            'countyCode': 'XYZ'
        }
        self.bad_data2 = {
            'countryCode': 'XY',
            'stateFipsCode': '64',
            'countyCode': '050'
        }
        self.bad_data3 = {
            'countryCode': 'FM',
            'stateFipsCode': 'XY',
            'countyCode': '050'
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_data))
        self.assertTrue(site_validator.validate(self.good_data2))
        self.assertTrue(site_validator.validate(self.good_data3))
        self.assertTrue(site_validator.validate(self.good_data4))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_data))
        self.assertFalse(site_validator.validate(self.bad_data2))
        self.assertFalse(site_validator.validate(self.bad_data3))


class ValidateStateCode(TestCase):

    def setUp(self):
        self.good_data = {
            'countryCode': 'FM',
            'stateFipsCode': '64',
        }
        self.good_data2 = {
            'countryCode': 'FM',
            'stateFipsCode': ' ',
        }
        self.good_data3 = {
            'countryCode': 'FM',
            'stateFipsCode': '',
        }
        self.good_data4 = {
            'countryCode': 'fm',
            'stateFipsCode': '64',
        }
        self.bad_data = {
            'countryCode': 'XY',
            'stateFipsCode': '64',
        }
        self.bad_data2 = {
            'countryCode': 'FM',
            'stateFipsCode': 'XY',
        }

    def test_validate_ok(self):
        self.assertTrue(site_validator.validate(self.good_data))
        self.assertTrue(site_validator.validate(self.good_data2))
        self.assertTrue(site_validator.validate(self.good_data3))
        self.assertTrue(site_validator.validate(self.good_data4))

    def test_with_validate_not_ok(self):
        self.assertFalse(site_validator.validate(self.bad_data))
        self.assertFalse(site_validator.validate(self.bad_data2))
