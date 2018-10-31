from unittest import TestCase

from ..cru_validator import CruValidator


class LocalDuplicateNormalizedStationNameTestCase(TestCase):
    """
    These are local tests; they don't rely on a real CRU endpoint
    """

    def setUp(self):
        # don't specify a real URL
        self.instance = CruValidator('')

    def test_make_duplicate_normalized_station_error_message(self):
        """
        Ensure that the error message has enough information to be helpful
        """
        station_normalized_name = 'MYSTATION'
        site_number = '1234567890'
        station = {
            "stationIx": station_normalized_name,
            "siteNumber": site_number
        }

        other_station_normalized_name = 'YOURSTATION'
        other_site_number = '0987654321'
        other_station = {
            "stationIx": other_station_normalized_name,
            "siteNumber": other_site_number
        }
        err = self.instance._make_duplicate_normalized_station_error_message(station, [other_station])
        self.assertIn(station_normalized_name, err)
        self.assertNotIn(site_number, err)
        self.assertIn(other_site_number, err)
        self.assertIn(other_station_normalized_name, err)

    def test_is_update(self):
        self.assertTrue(self.instance._is_update({'transactionType': 'M'}))
        self.assertFalse(self.instance._is_update({'transactionType': 'A'}))

    def test_update_mismatching_site_number(self):
        base_site = {
            "stationIx": "MYSTATION",
            "agencyCode": "USGS",
            "transactionType": "M"
        }
        station = {
            **base_site,
            "siteNumber": '1234567890',
        }

        other_station = {
            **base_site,
            "siteNumber": "0987654321",
        }
        valid = self.instance._validate_normalized_station_name(station, [other_station])
        self.assertFalse(valid)
        self.assertIn(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, self.instance.errors)

    def test_update_mismatching_agency_code(self):
        base_site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
            "transactionType": "M"
        }
        station = {
            **base_site,
            "agencyCode": "USGS",
        }

        other_station = {
            **base_site,
            "agencyCode": "EPA",
        }
        valid = self.instance._validate_normalized_station_name(station, [other_station])
        self.assertFalse(valid)
        self.assertIn(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, self.instance.errors)

    def test_update_matching_site_number_and_agency_code(self):
        base_site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
            "transactionType": "M",
            "agencyCode": "USGS"
        }
        station = {
            **base_site,
            "projectNumber": "1",
        }

        existing_station = {
            **base_site,
            "projectNumber": "2",
        }
        valid = self.instance._validate_normalized_station_name(station, [existing_station])
        self.assertTrue(valid)
        self.assertNotIn(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, self.instance.errors)

    def test_update_with_multiple_matching_sites(self):
        base_site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
            "transactionType": "M",
            "agencyCode": "USGS"
        }
        station = {
            **base_site,
            "projectNumber": "1",
        }

        existing_station0 = {
            **base_site,
            "projectNumber": "2",
        }
        existing_station1 = {
            **base_site,
            "projectNumber": "3",
        }
        valid = self.instance._validate_normalized_station_name(station, [existing_station0, existing_station1])
        self.assertFalse(valid)
        self.assertIn(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, self.instance.errors)

    def test_create_when_no_duplicates_exist(self):
        site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
            "transactionType": "A",
            "agencyCode": "USGS"
        }
        valid = self.instance._validate_normalized_station_name(site, [])
        self.assertTrue(valid)
        self.assertNotIn(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, self.instance.errors)

    def test_create_when_no_duplicates_exist(self):
        site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
            "transactionType": "A",
            "agencyCode": "USGS"
        }
        duplicate = site.copy()
        valid = self.instance._validate_normalized_station_name(site, [duplicate])
        self.assertFalse(valid)
        self.assertIn(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, self.instance.errors)

