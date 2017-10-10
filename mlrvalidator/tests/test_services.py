import json
from unittest import TestCase, mock

import yaml

import app


class AddValidateTransactionTestCase(TestCase):
    def setUp(self):
        app.application.testing = True
        self.app_client = app.application.test_client()
        self.location = {
            "ddotLocation" : {
                "agencyCode": "USGS ",
                "siteNumber": "123456789012345",
                "stationName": "This station name "
            },
            "existingLocation" : {}
        }

        self.bad_location = {
            "ddotLocation" : {
                "agencyCode": "USGS ",
                "siteNumber": " ",
                "stationName": "This station name "
            },
            "existingLocation" : {}
        }

        self.warning_location = {
            "ddotLocation": {
                "agencyCode": "USGS ",
                "siteNumber": "123456789012345",
                "stationName": "This station name '"
            },
            "existingLocation" : {}
        }

    def test_valid_single_field_transaction(self):
        with mock.patch('mlrvalidator.services.sitefile_single_field_validator.validate', return_value=True):
            response = self.app_client.post('/validators/add',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'validation_passed_message': 'Validations Passed'}, resp_data)

    def test_single_field_error_transaction(self):
        with mock.patch('mlrvalidator.services.sitefile_single_field_validator.validate', return_value=False):
            response = self.app_client.post('/validators/add',
                                        content_type='application/json',
                                        data=json.dumps(self.bad_location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'fatal_error_message': "Fatal Errors: {'siteNumber': ['Mandatory Field Missing']}"}, resp_data)

    def test_valid_reference_transaction(self):
        with mock.patch('mlrvalidator.services.sitefile_reference_validator.validate', return_value=True):
            response = self.app_client.post('/validators/add',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'validation_passed_message': 'Validations Passed'}, resp_data)

    def test_reference_error_transaction(self):
        with mock.patch('mlrvalidator.services.sitefile_reference_validator.validate', return_value=False):
            response = self.app_client.post('/validators/add',
                                        content_type='application/json',
                                        data=json.dumps(self.bad_location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'fatal_error_message': "Fatal Errors: {'siteNumber': ['Mandatory Field Missing']}"}, resp_data)

    def test_warning_transaction(self):
        with mock.patch('mlrvalidator.services.sitefile_warning_validator.validate', return_value=False):
            response = self.app_client.post('/validators/add',
                                        content_type='application/json',
                                        data=json.dumps(self.warning_location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'warning_message': 'Validation Warnings: {}'}, resp_data)

