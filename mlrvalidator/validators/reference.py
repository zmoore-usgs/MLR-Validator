import json

from mlrvalidator.utils import get_dict

class ReferenceInfo:
    def __init__(self, path_to_file):
        fd = open(path_to_file)
        with fd:
            self.reference_info = json.loads(fd.read())

    def get_reference_info(self):
        return self.reference_info



class CountryStateReference(ReferenceInfo):

    def get_list_by_country_state(self, attribute, country_code, state_code):
        country_list = self.reference_info['countries']
        state_list = get_dict(country_list, 'countryCode', country_code).get('states', [])

        return get_dict(state_list, 'stateFipsCode', state_code).get(attribute, [])



class Aquifers(CountryStateReference):
    def get_aquifers(self, country_code, state_code):
        return self.get_list_by_country_state('aquiferCodes', country_code, state_code)


class Hucs(CountryStateReference):
    def get_hucs(self, country_code, state_code):
        return self.get_list_by_country_state('hydrologicUnitCodes', country_code, state_code)


class Mcds(CountryStateReference):
    def get_mcds(self, country_code, state_code):
        return  self.get_list_by_country_state('minorCivilDivisionCodes', country_code, state_code)


class NationalAquifers(CountryStateReference):
    def get_national_aquifers(self, country_code, state_code):
        return self.get_list_by_country_state('nationalAquiferCodes', country_code, state_code)


class NationalWaterUseCodes(ReferenceInfo):
    def get_national_water_use_codes(self, site_type_code):
        site_type_list = self.reference_info['siteTypeCodes']
        return get_dict(site_type_list, 'siteTypeCode', site_type_code).get('nationalWaterUseCodes', [])


class Counties(CountryStateReference):
    def get_county_codes(self, country_code, state_code):
        county_list = self.get_list_by_country_state('counties', country_code, state_code)
        return [d.get('countyCode', '') for d in county_list]

    def get_county_attributes(self, country_code, state_code, county_code):
        country_list = self.get_list_by_country_state('counties', country_code, state_code)
        return get_dict(country_list, 'countyCode', county_code)


class States(CountryStateReference):

    def get_state_codes(self, country_code):
        country_list = self.reference_info['countries']
        state_list = get_dict(country_list, 'countryCode', country_code).get('states', [])
        state_code_list = [d['stateFipsCode'] for d in state_list]

        return state_code_list

    def get_state_attributes(self, country_code, state_code):
        country_list = self.reference_info['countries']
        state_list = get_dict(country_list, 'countryCode', country_code).get('states', [])
        return get_dict(state_list, 'stateFipsCode', state_code)


class FieldTransitions(ReferenceInfo):

    def get_allowed_transitions(self, existing_field_value):
        '''
        :return list of allowed new values. Return an empty list if the existing_field_value isn't in the reference list.
        :param string existing_field_value:
        '''
        return get_dict(self.reference_info, 'existingField', existing_field_value).get('newFields', [])


class SiteTypesCrossField(ReferenceInfo):

    def get_site_type_field_dependencies(self, site_type_code):
        site_type_cross_field_refs = self.reference_info['siteTypeCodes']
        try:
            site_type_field_ref = next((site_type_d for site_type_d in site_type_cross_field_refs if site_type_d['siteTypeCode'] == site_type_code.strip()))
        except StopIteration:
            site_type_field_ref = {'siteTypeCode': site_type_code, 'notNullAttrs': [], 'nullAttrs': []}
        return site_type_field_ref
