from unittest import TestCase

from ..cru_validator import CruValidator
import requests_mock
import json


class BaseDuplicateNormalizedStationNameTestCase(TestCase):
    """
    Utility methods for other test cases on duplicate normalized station names
    """
    def assertInvalid(self, valid):
        self.assertFalse(valid)
        self.assertIn(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, self.instance.errors)

    def assertValid(self, valid):
        self.assertTrue(valid)
        self.assertNotIn(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, self.instance.errors)


class LocalDuplicateNormalizedStationNameTestCase(BaseDuplicateNormalizedStationNameTestCase):
    """
    These are local tests; they avoid making any calls to methods that would hit the network
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
        self.assertInvalid(valid)

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
        self.assertInvalid(valid)

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
        self.assertValid(valid)

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
        self.assertInvalid(valid)

    def test_create_when_no_duplicates_exist(self):
        site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
            "transactionType": "A",
            "agencyCode": "USGS"
        }
        valid = self.instance._validate_normalized_station_name(site, [])
        self.assertValid(valid)

    def test_create_when_no_duplicates_exist(self):
        site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
            "transactionType": "A",
            "agencyCode": "USGS"
        }
        duplicate = site.copy()
        valid = self.instance._validate_normalized_station_name(site, [duplicate])
        self.assertInvalid(valid)

class DuplicateNormalizedStationNameTestCaseWithMockedCruService(BaseDuplicateNormalizedStationNameTestCase):
    """
    These are local tests; they rely on a mocked CRU endpoint
    """

    def setUp(self):
        # don't specify a real URL
        self.instance = CruValidator('http://localhost')

    @requests_mock.Mocker()
    def test_create_with_no_duplicates(self, mocker):
        mocker.get(requests_mock.ANY, status_code=404, text="[]")
        site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
            "transactionType": "A",
            "agencyCode": "USGS"
        }
        valid = self.instance.validate(site)
        self.assertValid(valid)

    @requests_mock.Mocker()
    def test_create_with_duplicate(self, mocker):

        base_site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
            "agencyCode": "USGS"
        }
        existing_site = base_site.copy()
        site = {
            **base_site,
            "transactionType": "A",
        }

        mock_response = json.dumps([existing_site])
        mocker.get(requests_mock.ANY, status_code=200, text=mock_response)

        valid = self.instance.validate(site)
        self.assertInvalid(valid)

    @requests_mock.Mocker()
    def test_update_existing(self, mocker):

        base_site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
            "agencyCode": "USGS"
        }

        existing_site = {
            **base_site,
            "projectNumber": "1",
        }

        updated_site = {
            **base_site,
            "projectNumber": "2",
            "transactionType": "M",

        }

        mock_response = json.dumps([existing_site])
        mocker.get(requests_mock.ANY, status_code=200, text=mock_response)

        valid = self.instance.validate(updated_site)
        self.assertValid(valid)

    @requests_mock.Mocker()
    def test_update_multiple_existing(self, mocker):

        base_site = {
            "stationIx": "MYSTATION",
            "siteNumber": "1234567890",
        }

        existing_site0 = {
            **base_site,
            "agencyCode": "USGS"

        }
        existing_site1 = {
            **base_site,
            "agencyCode": "EPA",

        }

        updated_site = {
            **base_site,
            "agencyCode": "MNPCA",
            "transactionType": "M",
        }

        mock_response = json.dumps([existing_site0, existing_site1])
        mocker.get(requests_mock.ANY, status_code=200, text=mock_response)

        valid = self.instance.validate(updated_site)
        self.assertInvalid(valid)

    @requests_mock.Mocker()
    def test_update_existing_different_site(self, mocker):
        base_site = {
            "stationIx": "MYSTATION",
        }

        existing_site = {
            **base_site,
            "siteNumber": "1234567890",
            "agencyCode": "USGS"
        }

        updated_site = {
            **base_site,
            "siteNumber": "0987654321",
            "agencyCode": "EPA",
            "transactionType": "M",
        }

        mock_response = json.dumps([existing_site])
        mocker.get(requests_mock.ANY, status_code=200, text=mock_response)

        valid = self.instance.validate(updated_site)
        self.assertInvalid(valid)