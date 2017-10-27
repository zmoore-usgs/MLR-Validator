
from collections import defaultdict
import os
import re

from .base_cross_field_validator import BaseCrossFieldValidator
from .country_state_reference_validator import CountryStateReferenceValidator
from .reference import States, NationalWaterUseCodes, SiteTypesCrossField, Counties, LandNetCrossField

class CrossFieldRefErrorValidator(BaseCrossFieldValidator):

    def __init__(self, reference_dir):
        super().__init__()
        self.aquifer_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'aquifer.json'), 'aquiferCodes', 'aquiferCode')
        self.huc_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'huc.json'), 'hydrologicUnitCodes', 'hydrologicUnitCode')
        self.mcd_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'mcd.json'), 'minorCivilDivsionCodes', 'minorCivilDivisionCode')
        self.national_aquifer_ref_validator = CountryStateReferenceValidator(os.path.join(reference_dir, 'national_aquifer.json'), 'nationalAquiferCodes', 'nationalAquiferCode')

        self.counties_ref = Counties(os.path.join(reference_dir, 'county.json'), 'counties')
        self.states_ref = States(os.path.join(reference_dir, 'state.json'))
        self.national_water_use_ref = NationalWaterUseCodes(os.path.join(reference_dir, 'national_water_use.json'))
        self.land_net_ref = LandNetCrossField(os.path.join(reference_dir, 'land_net.json'))
        self.site_type_ref = SiteTypesCrossField(os.path.join(reference_dir, 'site_type_cross_field.json'))



    def _validate_counties(self):
        keys = ['countryCode', 'stateFipsCode', 'countyCode']
        if self._any_fields_in_document(keys):
            country, state, county = [self.merged_document.get(key, '').strip() for key in keys]

            if country and state and county:
                county_list = self.counties_ref.get_county_codes(country, state)
                if county_list and county not in county_list:
                    self._errors['countyCode'] = ['County {0} is not in the reference list for country {1} and state {2}'.format(county, country, state)]

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
                    self._errors['stateFipsCode'] = ['{0} is not in the reference list for country {1}.'.format(state, country)]


    def _validate_national_water_use_code(self):
        '''
        :return: boolean
        '''
        keys = ['siteTypeCode', 'nationalWaterUseCode']
        if self._any_fields_in_document(keys):
            site_type, water_use = [self.merged_document.get(key, '').strip() for key in keys]

            if site_type and water_use:
                if water_use not in self.national_water_use_ref.get_national_water_use_codes(site_type):
                    self._errors['nationalWaterUseCode'] = ['{0} is not in the references list for siteTypeCode {1}'.format(water_use, site_type)]

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
            not_null_errors = []
            null_errors = []
            for not_null_attr in not_null_attrs:
                if not self.merged_document.get(not_null_attr, '').strip():
                    not_null_errors.append(not_null_attr)

            for null_attr in null_attrs:
                if self.merged_document.get(null_attr, '').strip():
                    null_errors.append(null_attr)

            if not_null_errors or null_errors:
                self._errors['siteTypeCode'] = []
                if not_null_errors:
                    self._errors['siteTypeCode'].append(
                        'Site type {0} must not have the following attributes null: {1}'.format(site_type, ', '.join(not_null_errors)))
                if null_errors:
                    self._errors['siteTypeCode'].append(
                        'Site type {0} must have the following attributes null: {1}'.format(site_type, ', '.join(null_errors)))

    def _validate_land_net(self):
        # Check that the land net description field follows the correct template

        """
        The rule's arguments are validated against this schema:
        {'valid_land_net': True}
        """
        error_message = "Invalid format - Land Net does not fit template"

        keys = ['districtCode', 'landNet']
        if self._any_fields_in_document(keys):
            district_code, land_net = [self.merged_document.get(key, '') for key in keys]

            if district_code and land_net:
                land_net_template = self.land_net_ref.get_land_net_templates(district_code)
                if land_net_template:
                    value_end = len(land_net) - 1
                    section = land_net_template.index("S")
                    township = land_net_template.index("T")
                    lrange = land_net_template.index("R")
                    try:
                        if land_net[section] == "S" and land_net[township] == "T" and land_net[lrange] == "R":
                            test_match = re.search('[^a-zA-Z0-9 ]', land_net[section:value_end])
                            if test_match is not None:
                                self._errors['landNet'] = [error_message]
                        else:
                            self._errors['landNet'] = [error_message]
                    except IndexError:
                        self._errors['landNet'] = [error_message]

    def validate(self, document, existing_document):
        '''
        :param dict document:
        :param dict existing_document:
        :return: boolean
        '''
        super().validate(document, existing_document)

        self.aquifer_ref_validator.validate(document, existing_document)
        # A huc of 99999999 is always allowed
        if self.merged_document.get('hydrologicUnitCode', '').strip() != '99999999':
            self.huc_ref_validator.validate(document, existing_document)
        self.mcd_ref_validator.validate(document, existing_document)
        self.national_aquifer_ref_validator.validate(document, existing_document)

        self._validate_counties()
        self._validate_states()
        self._validate_national_water_use_code()
        self._validate_site_type()
        self._validate_land_net()

        self._errors.update(self.aquifer_ref_validator.errors)
        self._errors.update(self.huc_ref_validator.errors)
        self._errors.update(self.mcd_ref_validator.errors)
        self._errors.update(self.national_aquifer_ref_validator.errors)

        return self._errors == {}

    @property
    def errors(self):
        return self._errors