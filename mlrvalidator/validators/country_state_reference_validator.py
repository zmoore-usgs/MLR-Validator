

from .reference import CountryStateReference
from .base_cross_field_validator import BaseCrossFieldValidator

class CountryStateReferenceValidator(BaseCrossFieldValidator):

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

        super().__init__()

    def validate(self, document, existing_document):
        """

        :param dict document:
        :param dict existing_document:
        :return: boolean
        The object's errors property will contain a dictionary describing the error if the validation is False
        """
        super().validate(document, existing_document)
        keys = ['countryCode', 'stateFipsCode', self.document_key]
        if self._any_fields_in_document(keys):
            country, state, value_to_check = [self.merged_document.get(key, '').strip() for key in keys]

            if country and state and value_to_check:
                ref_list = self.country_state_ref.get_list_by_country_state(country, state)
                if value_to_check not in ref_list:
                    self._errors.append({
                        self.document_key: '{0} is not in the reference list for country {1}, state {2}'.format(value_to_check, country, state)})


        return self._errors == []

    @property
    def errors(self):
        return self._errors



