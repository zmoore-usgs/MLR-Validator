
from unittest import TestCase

from ..cross_field_error_validator import CrossFieldErrorValidator


class LocationReciprocalDependencyTestCase(TestCase):

    def setUp(self):
        self.validator = CrossFieldErrorValidator()

    def test_all_non_null(self):
        self.assertTrue(self.validator.validate(
            {'latitude': 'A', 'longitude': 'B', 'coordinateAccuracyCode': 'C', 'coordinateDatumCode': 'D', 'coordinateMethodCode': 'E'},
            {}
        ))
        self.assertTrue(self.validator.validate(
            {'latitude': 'A', 'longitude': 'B', 'coordinateAccuracyCode': 'C'},
            {'coordinateDatumCode': 'D','coordinateMethodCode': 'E'}
        ))

    def test_all_null(self):
        self.assertTrue(self.validator.validate(
            {'latitude': '    ', 'longitude':'   '},
            {}
        ))
        self.assertTrue(self.validator.validate(
            {'latitude': '    ', 'longitude': '   '},
            {'latitude': 'A', 'coordinateDatumCode': ' ', 'coordinateDatumCode': ' ','coordinateMethodCode': ' '}
        ))

    def test_some_null(self):
        self.assertFalse(self.validator.validate(
            {'latitude': 'A', 'longitude': 'B', 'coordinateDatumCode': 'D', 'coordinateMethodCode': 'E'},
            {}
        ))
        self.assertIn('location', self.validator.errors)

        self.assertFalse(self.validator.validate(
            {'longitude': 'B', 'coordinateDatumCode': 'D', 'coordinateMethodCode': 'E'},
            {'latitude': '  '}
        ))
        self.assertIn('location', self.validator.errors)

    def test_no_fields_in_document(self):
        self.assertTrue(self.validator.validate(
            {},
            {'latitude': 'A', 'longitude': 'B', 'coordinateDatumCode': 'D', 'coordinateMethodCode': 'E'}
        ))


class AltitudeReciprocalDependencyTestCase(TestCase):

    def setUp(self):
        self.validator = CrossFieldErrorValidator()

    def test_all_non_null(self):
        self.assertTrue(self.validator.validate(
            {'altitude': 'A', 'altitudeDatumCode': 'B', 'altitudeMethodCode': 'C', 'altitudeAccuracyValue': 'D'},
            {}
        ))
        self.assertTrue(self.validator.validate(
            {'altitude': 'A', 'altitudeDatumCode': 'B'},
            {'altitudeMethodCode': 'C', 'altitudeAccuracyValue': 'D'}
        ))

    def test_all_null(self):
        self.assertTrue(self.validator.validate(
            {'altitude': ' ', 'altitudeDatumCode': ' ', 'altitudeAccuracyValue': ' '},
            {}
        ))
        self.assertTrue(self.validator.validate(
            {'altitude': ' ', 'altitudeMethodCode': ' ', 'altitudeAccuracyValue': ' '},
            {'altitude': 'A', 'altitudeDatumCode': '  '}
        ))

    def test_some_null(self):
        self.assertFalse(self.validator.validate(
            {'altitude': 'A', 'altitudeDatumCode': ' ', 'altitudeMethodCode': 'C', 'altitudeAccuracyValue': 'D'},
            {}
        ))
        self.assertIn('altitude', self.validator.errors)

        self.assertFalse(self.validator.validate(
            {'altitude': 'A', 'altitudeDatumCode': ' ', 'altitudeMethodCode': 'C', 'altitudeAccuracyValue': 'D'},
            {'altitudeDatumCode': 'A'}
        ))
        self.assertIn('altitude', self.validator.errors)

    def test_no_fields_in_document(self):
        self.assertTrue(self.validator.validate(
            {},
            {'altitude': 'A', 'altitudeDatumCode': ' ', 'altitudeMethodCode': 'C', 'altitudeAccuracyValue': 'D'}
        ))


class UseOfSiteTestCase(TestCase):

    def setUp(self):
        self.validator = CrossFieldErrorValidator()

    def test_all_valid(self):
        self.assertTrue(self.validator.validate(
            {'primaryUseOfSite': 'A', 'secondaryUseOfSite': 'B'},
            {'tertiaryUseOfSiteCode': 'C'}
        ))
        self.assertTrue(self.validator.validate(
            {'secondaryUseOfSite': 'B'},
            {'primaryUseOfSite': 'A', }
        ))

    def test_missing_primary(self):
        self.assertFalse(self.validator.validate(
            {'primaryUseOfSite': ' ', 'secondaryUseOfSite': 'B'},
            {}
        ))

        self.assertFalse(self.validator.validate(
            {'primaryUseOfSite': ' ', 'secondaryUseOfSite': 'B'},
            {'tertiaryUseOfSiteCode': 'C'}
        ))

    def test_missing_secondary(self):
        self.assertFalse(self.validator.validate(
            {'primaryUseOfSite': 'A ', 'secondaryUseOfSite': ' '},
            {'tertiaryUseOfSiteCode': 'C'}
        ))

    def test_non_unique_codes(self):
        self.assertFalse(self.validator.validate(
            {'primaryUseOfSite': 'A ', 'secondaryUseOfSite': 'B'},
            {'tertiaryUseOfSiteCode': 'B'}
        ))

        self.assertFalse(self.validator.validate(
            {'primaryUseOfSite': 'A ', 'secondaryUseOfSite': 'A'},
            {'tertiaryUseOfSiteCode': '  '}
        ))


class UseOfWaterCodeTestCase(TestCase):

    def setUp(self):
        self.validator = CrossFieldErrorValidator()

    def test_all_valid(self):
        self.assertTrue(self.validator.validate(
            {'primaryUseOfWaterCode': 'A', 'secondaryUseOfWaterCode': 'B'},
            {'tertiaryUseOfWaterCode': 'C'}
        ))
        self.assertTrue(self.validator.validate(
            {'secondaryUseOfWaterCode': 'B'},
            {'primaryUseOfWaterCode': 'A', }
        ))

    def test_missing_primary(self):
        self.assertFalse(self.validator.validate(
            {'primaryUseOfWaterCode': ' ', 'secondaryUseOfWaterCode': 'B'},
            {}
        ))

        self.assertFalse(self.validator.validate(
            {'primaryUseOfWaterCode': ' ', 'secondaryUseOfWaterCode': 'B'},
            {'tertiaryUseOfWaterCode': 'C'}
        ))

    def test_missing_secondary(self):
        self.assertFalse(self.validator.validate(
            {'primaryUseOfWaterCode': 'A ', 'secondaryUseOfWaterCode': ' '},
            {'tertiaryUseOfWaterCode': 'C'}
        ))

    def test_non_unique_codes(self):
        self.assertFalse(self.validator.validate(
            {'primaryUseOfWaterCode': 'A ', 'secondaryUseOfWaterCode': 'B'},
            {'tertiaryUseOfWaterCode': 'B'}
        ))

        self.assertFalse(self.validator.validate(
            {'primaryUseOfWaterCode': 'A ', 'secondaryUseOfWaterCode': 'A'},
            {'tertiaryUseOfWaterCode': '  '}
        ))


class SiteDatesTestCase(TestCase):
    def setUp(self):
        self.validator = CrossFieldErrorValidator()

    def test_valid_dates(self):
        self.assertTrue(self.validator.validate({'firstConstructionDate': '20100415', 'siteEstablishmentDate': '20100416'}, {}))
        self.assertTrue(self.validator.validate({'firstConstructionDate': '201004', 'siteEstablishmentDate': '20100416'}, {}))
        self.assertTrue(self.validator.validate({'firstConstructionDate': '2010'}, {'siteEstablishmentDate': '20100416'}))
        self.assertTrue(self.validator.validate({'firstConstructionDate': '2010', 'siteEstablishmentDate': '201004'}, {}))

    def test_with_empty_date(self):
        self.assertTrue(self.validator.validate({'firstConstructionDate': '20100415'}, {}))
        self.assertTrue(self.validator.validate({'siteEstablishmentDate': '20100415'}, {}))

    def test_with_invalid_dates(self):
        self.assertFalse(
            self.validator.validate({'firstConstructionDate': '20100415', 'siteEstablishmentDate': '20100414'}, {}))
        self.assertFalse(
            self.validator.validate({'firstConstructionDate': '201004', 'siteEstablishmentDate': '20100315'}, {}))
        self.assertFalse(
            self.validator.validate({'firstConstructionDate': '2010', 'siteEstablishmentDate': '20091231'}, {}))

    def test_with_missing_dates(self):
        self.assertTrue(self.validator.validate({'field1': 1}, {}))


class DepthsTestCase(TestCase):
    def setUp(self):
        self.validator = CrossFieldErrorValidator()

    def test_valid_depths(self):
        self.assertTrue(self.validator.validate({'wellDepth': '1234', 'holeDepth': '11234'}, {}))
        self.assertTrue(self.validator.validate({'wellDepth': '9'}, {'holeDepth': '10'}))

    def test_with_empty_depths(self):
        self.assertTrue(self.validator.validate({'wellDepth': '1234'}, {}))
        self.assertTrue(self.validator.validate({'holeDepth': '11234'}, {}))
        self.assertTrue(self.validator.validate({'holeDepth': ' '}, {'wellDepth': ' ', }))
        self.assertTrue(self.validator.validate({'wellDepth': '1234'}, {'holeDepth': 'A'}))

    def test_invalid_depths(self):
        self.assertFalse(self.validator.validate({'wellDepth': '11234', 'holeDepth': '1234'}, {}))
        self.assertFalse(self.validator.validate({'wellDepth': '10', 'holeDepth': '9'}, {}))

