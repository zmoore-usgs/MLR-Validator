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

    def __init__(self, path_to_file, ref_list_key):
        '''
        The json in the files is assumed to have the following form:
        {"countries": [{"countryCode: "BG", "states": [{"stateFipsCode": "01", "ref_list_key": ["A", "B"]}]}]}'
        :param str path_to_file:
        :param str ref_list_key: Key of the list to return when searching by country and state.
        '''
        self.ref_list_key = ref_list_key
        super().__init__(path_to_file)

    def get_list_by_country_state(self, country_code, state_code):
        country_list = self.reference_info['countries']
        state_list = get_dict(country_list, 'countryCode', country_code).get('states', [])

        return get_dict(state_list, 'stateFipsCode', state_code).get(self.ref_list_key, [])


class NationalWaterUseCodes(ReferenceInfo):
    def get_national_water_use_codes(self, site_type_code):
        site_type_list = self.reference_info['siteTypeCodes']
        return get_dict(site_type_list, 'siteTypeCode', site_type_code).get('nationalWaterUseCodes', [])


class Counties(CountryStateReference):

    def __init__(self, path_to_file):
        super().__init__(path_to_file, 'counties')


    def get_county_codes(self, country_code, state_code):
        county_list = self.get_list_by_country_state(country_code, state_code)
        county_code_list = [d['countyCode'] for d in county_list]

        return county_code_list

    def get_county_attributes(self, country_code, state_code, county_code):
        county_list = self.get_list_by_country_state(country_code, state_code)
        try:
            county_attributes = list(filter(lambda cc: cc['countyCode'] == county_code, county_list))[0]
        except IndexError:
            county_attributes = {}

        return county_attributes


class States(ReferenceInfo):

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


class LandNetCrossField(ReferenceInfo):

    def get_land_net_templates(self, district_code):
        land_net_templates = self.reference_info['landNetTemplates']
        try:
            land_net_template = get_dict(land_net_templates, 'districtCode', district_code.strip()).get('landNetTemplate', {})
        except StopIteration:
            land_net_template = {}
        return land_net_template


class SiteNumberFormat(ReferenceInfo):
    def get_site_number_template(self, site_type_code):
        site_number_format_refs = self.reference_info['siteNumberFormatCodes']

        try:
            idx = next(index for (index, d) in enumerate(site_number_format_refs) if site_type_code in d['siteTypeCode'])
            site_number_format_ref = site_number_format_refs[idx]['siteNumberFormatCode']
        except StopIteration:
            site_number_format_ref = ''
        return site_number_format_ref

