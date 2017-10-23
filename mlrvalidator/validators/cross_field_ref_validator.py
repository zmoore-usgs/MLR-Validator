
from collections import defaultdict
import os

from .base_cross_field_validator import BaseCrossFieldValidator
from .country_state_reference_validator import CountryStateReferenceValidator
from .reference import States, NationalWaterUseCodes, SiteTypesCrossField

class CrossFieldRefValidator(BaseCrossFieldValidator):

    def __init__(self, reference_dir):
        super().__init__()
        self.aquifer_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'aquifer.json'), 'aquiferCodes, aquiferCode')
        self.huc_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'huc.json'), 'hydrologicUnitCodes', 'hydrologicUnitCode')
        self.mcd_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'mcd.json'), 'minorCivilDivsionCodes', 'minorCivilDivisionCode')
        self.national_aquifer_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'national_aquifer.json'), 'nationalAquiferCodes', 'nationalAquiferCode')
        self.counties_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'county.json'), 'counties', 'countyCode')

        self.states_ref = States(os.path.join(reference_dir, 'state.json'))
        self.national_water_use_ref = NationalWaterUseCodes(os.path.join(reference_dir, 'national_water_us.json'))
        self.site_type_ref = SiteTypesCrossField(os.path.join(reference_dir, 'site_type_cross_field.json'))


    def _validate_states(self):
        '''
        :return: boolean
        '''
        keys = ['countryCode', 'stateFipsCode']
        if self._any_fields_in_document(keys):
            country, state = [self.merged_document.get(key, '').strip() for key in keys]

            if country and state:
                state_list = self.states_ref.get_state_codes(country)
                if state_list and state not in state_list:
                    self._errors.append({'stateFipsCode': '{0} is not in the reference list for country {1}.'.format(state, country)})


    def _validate_national_water_use_code(self):
        '''
        :return: boolean
        '''
        keys = ['siteTypeCode', 'nationalWaterUseCode']
        if self._any_fields_in_document(keys):
            site_type, water_use = [self.merged_document.get(key, '').strip() for key in keys]

            if site_type and water_use:
                if water_use not in self.national_water_use_ref.get_national_water_use_codes(site_type):
                    self._errors.append({'nationalWaterUseCode': '{0} is not in the referces list for siteTypeCode {1}'.format(water_use, site_type)})

    def _validate_site_type(self):
        site_type = self.merged_document.get('siteTypeCode', '').strip()

        if site_type:
            site_type_attr = self.site_type_ref.get_site_type_field_dependencies(site_type)
            if 'siteTypeCode' in self.document:
                # Should check all fields in site_type_attr
                not_null_attrs = site_type_attr.get('notNullAttrs', [])
                null_attrs = site_type_attr.get('nullAttrs', [])
            else:
                # Only check fields that are in the document
                not_null_attrs = [not_null_attr for not_null_attr in site_type_attr.get('notNullAttrs', [])
                                  if not_null_attr in self.document]
                null_attrs = [null_attr for null_attr in site_type_attr.get('nullAttrs', [])
                              if null_attr in self.document]

            # Should check all fields in site_type_attr
            for not_null_attr in not_null_attrs:
                if not self.merged_document.get(not_null_attr, '').strip():
                    self._errors.append(
                        {not_null_attr: 'The field must not be null for site type {0}'.format(site_type)})

            for null_attr in null_attrs:
                if self.merged_document.get(null_attr, '').strip():
                    self._errors.append({null_attr: 'The field must be null for site type {0}'.format(site_type)})

    def validate(self, document, existing_document):
        '''
        :param dict document:
        :param dict existing_document:
        :return: boolean
        '''
        super().validate(document, existing_document)

        self.aquifer_ref_validator.validate(document, existing_document)
        self.huc_ref_validator.validate(document, existing_document)
        self.mcd_ref_validator.validate(document, existing_document)
        self.national_aquifer_ref_validator.validate(document, existing_document)
        self.counties_ref_validator.validate(document, existing_document)

        self._validate_states()
        self._validate_national_water_use_code()
        self._validate_site_type()

        self._errors.extend(self.aquifer_ref_validator.errors)
        self._errors.extend(self.huc_ref_validator.errors)
        self._errors.extend(self.huc_ref_validator.errors)
        self._errors.extend(self.national_aquifer_ref_validator.errors)
        self._errors.extend(self.counties_ref_validator.errors)

        return self._errors == []

    @property
    def errors(self):
        return self._errors