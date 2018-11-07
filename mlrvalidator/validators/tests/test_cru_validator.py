from unittest import TestCase

from ..cru_validator import CruValidator
import requests_mock
import json


class DuplicateNormalizedStationNameTestCase(TestCase):
    """
    These are local tests; they rely on a mocked CRU endpoint
    """

    def setUp(self):
        # don't specify a real URL
        self.instance = CruValidator('http://localhost')

    def assertInvalid(self, valid):
        self.assertFalse(valid)
        self.assertIn(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, self.instance.errors)

    def assertValid(self, valid):
        self.assertTrue(valid)
        self.assertNotIn(CruValidator.DUPLICATE_NORMALIZED_STATION_NAME, self.instance.errors)

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

    def test_create_with_missing_station_ix(self):
        site = {
            "siteNumber": "1234567890",
            "transactionType": "A",
            "agencyCode": "USGS"
        }
        valid = self.instance.validate(site)
        self.assertFalse(valid)
        self.assertIn(CruValidator.MISSING_NORMALIZED_STATION_NAME, self.instance.errors)

    @requests_mock.Mocker()
    def test_update_existing_keeping_station_ix_the_same(self, mocker):

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

        valid = self.instance.validate(updated_site, update=True)
        self.assertValid(valid)

    @requests_mock.Mocker()
    def test_update_existing_with_new_station_ix(self, mocker):
        updated_site = {
            "siteNumber": "1234567890",
            "agencyCode": "USGS",
            "stationIx": "MYSTATION",
            "projectNumber": "2",
            "transactionType": "M",

        }

        mocker.get(requests_mock.ANY, status_code=404, text="[]")

        valid = self.instance.validate(updated_site, update=True)
        self.assertValid(valid)

    @requests_mock.Mocker()
    def test_update_existing_with_non_station_name_attributes(self, mocker):

        base_site = {
            "siteNumber": "1234567890",
            "agencyCode": "USGS"
        }

        existing_site = {
            **base_site,
            "stationIx": "MYSTATION",
            "projectNumber": "1",
        }

        updated_site = {
            **base_site,
            "projectNumber": "2",
            "transactionType": "M",

        }

        mock_response = json.dumps([existing_site])
        mocker.get(requests_mock.ANY, status_code=200, text=mock_response)

        valid = self.instance.validate(updated_site, update=True)
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

        valid = self.instance.validate(updated_site, update=True)
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

        valid = self.instance.validate(updated_site, update=True)
        self.assertInvalid(valid)

    @requests_mock.Mocker()
    def test_update_ml_when_identifying_attributes_are_missing_from_existing_ml(self, mocker):
        base_site = {
            "stationIx": "MYSTATION",
        }

        existing_site = base_site.copy()

        updated_site = {
            **base_site,
            "siteNumber": "1234567890",
            "agencyCode": "USGS",
            "transactionType": "M",
        }

        mock_response = json.dumps([existing_site])
        mocker.get(requests_mock.ANY, status_code=200, text=mock_response)

        valid = self.instance.validate(updated_site, update=True)
        self.assertInvalid(valid)

    @requests_mock.Mocker()
    def test_update_ml_when_identifying_attributes_are_missing_from_proposal(self, mocker):
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
            "transactionType": "M",
        }

        mock_response = json.dumps([existing_site])
        mocker.get(requests_mock.ANY, status_code=200, text=mock_response)

        valid = self.instance.validate(updated_site, update=True)
        self.assertInvalid(valid)
