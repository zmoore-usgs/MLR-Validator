import json
import yaml
from unittest import TestCase, mock
import app
from validator import ValidateError


class AddValidateTransactionTestCase(TestCase):
    def setUp(self):
        app.application.testing = True
        self.app_client = app.application.test_client()
        self.schema = yaml.load(
            """
                    agencyCode:
                        is_empty: False
                        maxlength: 5
                    siteNumber:
                        maxlength: 15
                        is_empty: False
            """
            )
        self.validator = app.sitefile_validator
        self.location = {
            "agencyCode": "USGS ",
            "siteNumber": "123456789012345",
            "stationName": "This station name "
        }

    def test_valid_transaction(self):
        valid_result = "Validation Passed"
        with mock.patch('services.validate_data', return_value=valid_result):
            response = self.app_client.post('/validators',
                                        content_type='application/json',
                                        data=json.dumps(self.location))
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual({"success_message": "Validation Passed"}, resp_data)
