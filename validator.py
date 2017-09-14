
class ValidateError(Exception):
    def __init__(self, message):
        self.message = message


def validate(data, schema, site_validator):
    '''

    :param data:
    :param schema:
    :param site_validator
    :return: boolean True if validation successful
    :raises: ValidateError with an appropriate message if unable to validate data.
    '''

    result = site_validator.validate(data, schema)

    if not result:
        raise ValidateError('Validation Error: {0}'.format(site_validator.errors))

    return 'Validation Successful'
