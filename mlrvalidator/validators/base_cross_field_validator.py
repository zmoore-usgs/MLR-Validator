
class BaseCrossFieldValidator:
    '''
    Extends validate to add an argument for the existing_document. Typically for an add this will be empty.
    '''

    def __init__(self):
        self._errors = []

    def validate(self, document, existing_document):
        self.document = document
        self.existing_document = existing_document
        self.merged_document = existing_document.copy()
        self.merged_document.update(document)

        self._errors = []

        return True

    @property
    def errors(self):
        return self._errors

    def _any_fields_in_document(self, keys):
        '''

        :param list of str keys:
        :return: boolean
        '''
        document_keys = self.document.keys()
        return [key for key in keys if key in document_keys] != []

    def _validate_reciprocal_dependency(self, keys, error_key):
        '''
        If not all values null or all non null an error will be
        added to self._errors using error_key as the object key
        :param list of str keys:
        :param str error_key: key to be used if an error is found
        '''
        values = [self.merged_document.get(key, '').strip() for key in keys]
        all_null = [value for value in values if value != '' ] == []
        all_not_null = [value for value in values if value == ''] == []
        if not (all_null or all_not_null):
            self._errors.append(
                {error_key: 'The following fields must all be empty or all must not be empty: {0}'.format(', '.join(keys))}
            )



