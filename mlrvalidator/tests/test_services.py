import json
from unittest import TestCase, mock

from cerberus import Validator

import app

@mock.patch('app.sitefile_single_field_validator.validate', )
@mock.patch('app.sitefile_warning_validator.validate')
@mock.patch('app.sitefile_reference_validator.validate')
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


    def test_valid_transaction(self, msingle_field_validate, mwarning_validate, mreference_validate):
        msingle_field_validate.return_value = True
        mwarning_validate.return_value = True
        mreference_validate.return_value = True

        response = self.app_client.post('/validators/add',
                                    content_type='application/json',
                                    data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({'validation_passed_message': 'Validations Passed'}, resp_data)

    def test_single_field_error_transaction(self, msingle_field_validate, mwarning_validate, mreference_validate):
        msingle_field_validate.return_value = False
        mwarning_validate.return_value = True
        mreference_validate.return_value = True

        response = self.app_client.post('/validators/add',
                                    content_type='application/json',
                                    data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertIn('fatal_error_message', resp_data)


    def test_reference_error_transaction(self, msingle_field_validate, mwarning_validate, mreference_validate):
        msingle_field_validate.return_value = True
        mwarning_validate.return_value = True
        mreference_validate.return_value = False
        response = self.app_client.post('/validators/add',
                                    content_type='application/json',
                                    data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertIn('fatal_error_message', resp_data)


    def test_warning_transaction(self, msingle_field_validate, mwarning_validate, mreference_validate):
        msingle_field_validate.return_value = True
        mwarning_validate.return_value = False
        mreference_validate.return_value = True
        response = self.app_client.post('/validators/add',
                                    content_type='application/json',
                                    data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertIn('warning_message', resp_data)
