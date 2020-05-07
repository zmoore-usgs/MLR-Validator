
import os

from .reference import SiteTypeInvalidCodes, FieldTransitions

class TransitionValidator:

    def __init__(self, local_reference_dir):
        self._errors = {}
        self.site_type_invalid_code_list = []
        self.site_type_transition_ref = FieldTransitions(os.path.join(local_reference_dir, 'site_type_transition.json'))
        self.site_type_invalid_code_list = SiteTypeInvalidCodes(os.path.join(local_reference_dir, 'site_type_invalid.json'))

    def validate(self, document, existing_document):
        self._errors = {}

        existing_value = existing_document.get('siteTypeCode', '').strip()
        new_value = document.get('siteTypeCode', '').strip()

        if existing_value and new_value and (existing_value != new_value):
            transitions = self.site_type_transition_ref.get_allowed_transitions(existing_value)
            if transitions and transitions.count(new_value) == 0:
                self._errors['siteTypeCode'] = ['Can\'t change a siteTypeCode with existing value {0} to {1}'.format(existing_value, new_value)]
        
        invalid_codes = self.site_type_invalid_code_list.get_site_type_invalid_codes()
        if (existing_value in invalid_codes and new_value is '') or (new_value in invalid_codes):
            self._errors['siteTypeCode'] = ['Existing record uses a non-valid site type, may not use a non-valid code for site creation or updates. Re-submit with a valid siteTypeCode.']

        return self._errors == {}

    @property
    def errors(self):
        return self._errors