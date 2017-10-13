import json
from unittest import TestCase, mock

import app

@mock.patch('mlrvalidator.services.warning_validator')
@mock.patch('mlrvalidator.services.error_validator')
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


    def test_valid_transaction(self, merror_validator, mwarning_validator):
        merror_validator.validate.return_value = True
        merror_validator.errors = {}
        mwarning_validator.validate.return_value = True
        mwarning_validator.errors = {}

        response = self.app_client.post('/validators/add',
                                    content_type='application/json',
                                    data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        merror_validator.validate.assert_called_with(self.location.get('ddotLocation'))
        mwarning_validator.validate.assert_called_with(self.location.get('ddotLocation'))
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'validation_passed_message': 'Validations Passed'}, resp_data)

    def test_transaction_with_error(self, merror_validator, mwarning_validator):
        merror_validator.validate.return_value = False
        merror_validator.errors = {'stationName': ['Invalid value']}
        mwarning_validator.validate.return_value = True
        mwarning_validator.errors = {}

        response = self.app_client.post('/validators/add',
                                    content_type='application/json',
                                    data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertIn('fatal_error_message', resp_data)


    def test_transaction_with_warning(self, merror_validator, mwarning_validator):
        merror_validator.validate.return_value = True
        merror_validator.errors = {}
        mwarning_validator.validate.return_value = False
        mwarning_validator.errors = {'stationName': ['Contains quotes']}

        response = self.app_client.post('/validators/add',
                                    content_type='application/json',
                                    data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertIn('warning_message', resp_data)

    def test_transaction_with_error_and_warning(self, merror_validator, mwarning_validator):
        merror_validator.validate.return_value = False
        merror_validator.errors = {'agencyCode': ['Bad value']}
        mwarning_validator.validate.return_value = False
        mwarning_validator.errors = {'stationName': ['Contains quotes']}

        response = self.app_client.post('/validators/add',
                                    content_type='application/json',
                                    data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 2)
        self.assertIn('warning_message', resp_data)
        self.assertIn('fatal_error_message', resp_data)