
class ValidateError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'Validation Error: {0}'.format(self.message)


class ValidateWarning(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'Validation Warning: {0}'.format(self.message)


def validate(data, schema, site_validator, validation_type):
    '''

    :param data:
    :param schema:
    :param site_validator
    :param validation_type
    :return: boolean True if validation successful
    :raises: ValidateError with an appropriate message if validation failures exist.
    :raises: ValidateWarning with an appropriate message if validation warnings exist.
    '''

    if validation_type == 'error':
        result = site_validator.validate(data, schema)

        if not result:
            raise ValidateError('Validation Fatal Error: {0}'.format(site_validator.errors))

    elif validation_type == 'warning':
        result = site_validator.validate(data, schema)

        if not result:
            raise ValidateWarning('Validation Warning: {0}'.format(site_validator.errors))

    return 'Validation Passed'
