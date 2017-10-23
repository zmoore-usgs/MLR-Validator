
from .base_cross_field_validator import BaseCrossFieldValidator

class CrossFieldWarningValidator(BaseCrossFieldValidator):

    def __init__(self, states_reference):
        '''
        :param object states_reference: should be a references.States instance
        '''
        self.states_ref = states_reference

        super().__init__()

    def _validate_latitude_range(self):
        keys = ['latitude', 'countryCode', 'stateFipsCode']
        if self._any_fields_in_document(keys):
            lat, country, state = [self.merged_document.get(key, '').strip() for key in keys]

            if lat and country and state:
                # Do a check for lat range using the country and state codes
                state_attr = self.states_ref.get_state_attributes(country, state)
                if state_attr and 'state_min_lat_va' in state_attr and 'state_max_lat_va' in state_attr:
                    if not (state_attr['state_min_lat_va'] <= lat < state_attr['state_max_lat_va']):
                        self._errors.append({'latitude': 'Latitude is out of range for state {0}'.format(state)})

    def _validate_longitude_range(self):
        keys = ['longitude', 'countryCode', 'stateFipsCode']
        if self._any_fields_in_document(keys):
            lat, country, state = [self.merged_document.get(key, '').strip() for key in keys]

            if lat and country and state:
                # Do a check for lat range using the country and state codes
                state_attr = self.states_ref.get_state_attributes(country, state)
                if state_attr and 'state_min_long_va' in state_attr and 'state_max_long_va' in state_attr:
                    if not (state_attr['state_min_long_va'] <= lat < state_attr['state_max_long_va']):
                        self._errors.append({'longitude': 'Longitude is out of range for state {0}'.format(state)})


    def validate(self, document, existing_document):
        super().validate(document, existing_document)
        self._validate_latitude_range()
        self._validate_longitude_range()

        return self._errors == []




