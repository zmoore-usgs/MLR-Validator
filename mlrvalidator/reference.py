import os
import json

PROJECT_DIR = os.path.dirname(__file__)


class ReferenceInfo:
    def __init__(self, file_name):
        fd = open(os.path.join(PROJECT_DIR, file_name))
        with fd:
            self.reference_info = json.loads(fd.read())

    def get_reference_info(self):
        return self.reference_info

    def _get_reference_list(self, reference_attribute, parent_attribute, parent_value, parent_list):
        try:
            reference_object = list(filter(lambda c: c[parent_attribute] == parent_value, parent_list))[0]
        except IndexError:
            reference_list = []
        else:
            reference_list = reference_object[reference_attribute]
        return reference_list

    def get_list_by_country_state(self, attribute, country_code, state_code):
        country_list = self.reference_info['countries']
        state_list = self._get_reference_list('states', 'countryCode', country_code, country_list)
        attribute_list = self._get_reference_list(attribute, 'stateFipsCode', state_code, state_list)

        return attribute_list


class Aquifers(ReferenceInfo):
    def get_aquifers(self, country_code, state_code):
        aquifer_list = self.get_list_by_country_state('aquiferCodes', country_code, state_code)

        return aquifer_list


class Hucs(ReferenceInfo):
    def get_hucs(self, country_code, state_code):
        huc_list = self.get_list_by_country_state('hydrologicUnitCodes', country_code, state_code)

        return huc_list


class Mcds(ReferenceInfo):
    def get_mcds(self, country_code, state_code):
        mcd_list = self.get_list_by_country_state('minorCivilDivisionCodes', country_code, state_code)

        return mcd_list


class NationalAquifers(ReferenceInfo):
    def get_national_aquifers(self, country_code, state_code):
        national_aquifers_list = self.get_list_by_country_state('nationalAquiferCodes', country_code, state_code)

        return national_aquifers_list


class NationalWaterUseCodes(ReferenceInfo):
    def get_national_water_use_codes(self, site_type_code):
        site_type_list = self.reference_info['siteTypeCodes']
        national_water_use_code_list = self._get_reference_list('nationalWaterUseCodes', 'siteTypeCode', site_type_code, site_type_list)

        return national_water_use_code_list


class Counties(ReferenceInfo):
    def get_county_codes(self, country_code, state_code):
        county_list = self.get_list_by_country_state('counties', country_code, state_code)
        county_code_list = [d['countyCode'] for d in county_list]

        return county_code_list

    def get_county_attributes(self, country_code, state_code, county_code):
        county_list = self.get_list_by_country_state('counties', country_code, state_code)
        try:
            county_attributes = list(filter(lambda cc: cc['countyCode'] == county_code, county_list))[0]
        except IndexError:
            county_attributes = {}

        return county_attributes


class States(ReferenceInfo):
    def get_state_codes(self, country_code):
        country_list = self.reference_info['countries']
        state_list = self._get_reference_list('states', 'countryCode', country_code, country_list)
        state_code_list = [d['stateFipsCode'] for d in state_list]

        return state_code_list

    def get_state_attributes(self, country_code, state_code):
        country_list = self.reference_info['countries']
        state_list = self._get_reference_list('states', 'countryCode', country_code, country_list)
        try:
            state_attributes = list(filter(lambda s: s['stateFipsCode'] == state_code, state_list))[0]
        except IndexError:
            state_attributes = {}
        return state_attributes


class SiteTypes(ReferenceInfo):
    def get_site_types(self, old_site_type_code):
        old_site_types = self.reference_info['oldSiteTypeCodes']
        new_site_type_list = self._get_reference_list('newSiteTypeCodes', 'oldSiteTypeCode', old_site_type_code, old_site_types)

        return new_site_type_list


class SiteTypesCrossField(ReferenceInfo):

    def get_site_type_field_dependencies(self, site_type_code):
        site_type_cross_field_refs = self.reference_info['siteTypeCodes']
        site_type_field_ref = next((site_type_d for site_type_d in site_type_cross_field_refs if site_type_d['siteTypeCode'] == site_type_code))
        return site_type_field_ref
