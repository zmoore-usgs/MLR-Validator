
from collections import defaultdict
import os

from .country_state_reference_validator import CountryStateReferenceValidator
from .reference import States

class CrossFieldValidator:

    def __init__(self, reference_dir):
        self.aquifer_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'aquifer.json'), 'aquiferCodes, aquiferCode')
        self.huc_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'huc.json'), 'hydrologicUnitCodes', 'hydrologicUnitCode')
        self.mcd_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'mcd.json'), 'minorCivilDivsionCodes', 'minorCivilDivisionCode')
        self.national_aquifer_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'national_aquifer.json'), 'nationalAquiferCodes', 'nationalAquiferCode')
        self.counties_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'county.json'), 'counties', 'countyCode')

        self.states_ref = States(os.path.join(reference_dir, 'state.json'))

        self._errors = []

    def _validate_states(self):
        '''
        :return: boolean
        '''

        country = self.merged_document.get('countryCode', '').strip()
        state = self.merged_document.get('stateFipsCode', '').strip()

        valid = True
        if country and state:
            valid = self.state_ref.get_state_attributes(country, state) != {}
            if not valid:
                self._errors.append({'stateFipsCode': '{0} is not in the reference list for country {1}.'.format(state, country)})


        return valid

    def validate(self, document, existing_document):
        '''
        :param dict document:
        :param dict existing_document:
        :return: boolean
        '''
        self._errors = defaultdict(list)
        self.merged_document = existing_document.copy()
        self.merged_document.update(document)

        valid_aquifer = self.aquifer_ref_validator.validate(document, existing_document)
        valid_huc = self.huc_ref_validator.validate(document, existing_document)
        valid_mcd = self.mcd_ref_validator.validate(document, existing_document)
        valid_national_aquifer = self.national_aquifer_ref_validator.validate(document, existing_document)
        valid_counties = self.counties_ref_validator.validate(document, existing_document)

        valid_states = self._validate_states()

        self._errors.extend([self.aquifer_ref_validator.errors,
                             self.huc_ref_validator.errors,
                             self.mcd_ref_validator.errors,
                             self.national_aquifer_ref_validator.errors,
                             self.counties_ref_validator.errors,
                             ])

    @property
    def error(self):
        return self._errors