from cerberus import Validator
import json


class ValidateError(Exception):
    def __init__(self, message):
        self.message = message


def validate(data, schema):
    '''

    :param data:
    :param schema:
    :return: boolean True if validation successful
    :raises: ValidateError with an appropriate message if unable to validate data.
    '''

    v = Validator()
    v.allow_unknown = True
    result = v.validate(data, schema)

    if not result:
        raise ValidateError('Validation Error: {0}'.format(v.errors))

    return 'Validation Successful'
