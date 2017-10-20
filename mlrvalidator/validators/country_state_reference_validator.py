

from .reference import CountryStateReference

class CountryStateReferenceValidator:

    def __init__(self, path_to_reference_file, ref_list_key, document_key):
        '''

        :param str path_to_reference_file:
        :param str ref_list_key: key to use in reference list.
        :param str document_key: key to use in the merged document to get the value to match
        '''
        self.country_state_ref = CountryStateReference(path_to_reference_file, ref_list_key)
        self.document_key = document_key
        self.country_key = 'countryCode'
        self.state_key = 'stateFipsCode'

        self._errors = None

    def validate(self, document, existing_document):
        """

        :param dict document:
        :param dict existing_document:
        :return: boolean
        The object's errors property will contain a dictionary describing the error if the validation is False
        """
        self._errors = None

        if any(key in document for key in [self.document_key, self.country_key, self.state_key]):
            merged_document = existing_document.copy()
            merged_document.update(document)

            country = merged_document.get(self.country_key, '').strip()
            state = merged_document.get(self.state_key, '').strip()
            value_to_check = merged_document.get(self.document_key, '').strip()

            if country and state and value_to_check:
                ref_list = self.country_state_ref.get_list_by_country_state(country, state)
                if value_to_check not in ref_list:
                    self._errors = {
                        self.document_key: '{0} is not in the reference list for country {1}, state {2}'.format(value_to_check, country, state)}


        return self._errors is None

    @property
    def errors(self):
        return self._errors



