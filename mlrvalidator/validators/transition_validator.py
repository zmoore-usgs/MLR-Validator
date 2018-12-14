
import os

from .reference import ReferenceInfo, FieldTransitions

class TransitionValidator:

    def __init__(self, reference_dir):
        self._errors = {}
        self.site_type_transition_ref = FieldTransitions(os.path.join(reference_dir, 'site_type_transition.json'))
        self.reference_lists = ReferenceInfo(os.path.join(reference_dir, 'reference_lists.json'))
        self.site_type_invalid_code_list = self.reference_lists.get_reference_info().get('siteTypeInvalidCode', [])

    def validate(self, document, existing_document):
        self._errors = {}
        existing_value = existing_document.get('siteTypeCode', '').strip()
        new_value = document.get('siteTypeCode', '').strip()

        if existing_value and new_value and (existing_value != new_value):
            transitions = self.site_type_transition_ref.get_allowed_transitions(existing_value)
            if transitions and transitions.count(new_value) == 0:
                self._errors['siteTypeCode'] = ['Can\'t change a siteTypeCode with existing value {0} to {1}'.format(existing_value, new_value)]

        if existing_value in self.site_type_invalid_code_list and new_value is '' or new_value in self.site_type_invalid_code_list:
            self._errors['siteTypeCode'] = ['Existing record uses a non-valid site type, may not use a non-valid code for site creation or updates. Re-submit with a valid siteTypeCode.']

        return self._errors == {}

    @property
    def errors(self):
        return self._errors