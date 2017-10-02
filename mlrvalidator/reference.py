import os
import json

PROJECT_DIR = os.path.dirname(__file__)


def get_aquifers(country_code, state_code):
    try:
        aquifer_file = open(os.path.join(PROJECT_DIR, 'references/aquifer.json'))
        with aquifer_file:
            aquifer = json.loads(aquifer_file.read())
        country_list = aquifer['countries']
        country = list(filter(lambda c: c['countryCode'] == country_code, country_list))[0]
        state_list = country['states']
        state = list(filter(lambda s: s['stateFipsCode'] == state_code, state_list))[0]
        aquifer_list = state['aquiferCodes']
    except IndexError:
        aquifer_list = []
    return aquifer_list


county_file = open(os.path.join(PROJECT_DIR, 'references/county.json'))
with county_file:
    county_json = json.loads(county_file.read())


def get_county_codes(country_code, state_code):
    try:
        country_list = county_json['countries']
        country = list(filter(lambda c: c['countryCode'] == country_code, country_list))[0]
        state_list = country['states']
        state = list(filter(lambda s: s['stateFipsCode'] == state_code, state_list))[0]
        county_list = state['counties']
        county_code_list = [d['countyCode'] for d in county_list]
    except IndexError:
        county_code_list = []
    return county_code_list


def get_county_attributes(country_code, state_code, county_code):
    try:
        country_list = county_json['countries']
        country = list(filter(lambda c: c['countryCode'] == country_code, country_list))[0]
        state_list = country['states']
        state = list(filter(lambda s: s['stateFipsCode'] == state_code, state_list))[0]
        county_list = state['counties']
        county_attributes = list(filter(lambda cc: cc['countyCode'] == county_code, county_list))[0]
    except IndexError:
        county_attributes = {}
    return county_attributes


def get_hucs(country_code, state_code):
    try:
        huc_file = open(os.path.join(PROJECT_DIR, 'references/huc.json'))
        with huc_file:
            huc = json.loads(huc_file.read())
        country_list = huc['countries']
        country = list(filter(lambda c: c['countryCode'] == country_code, country_list))[0]
        state_list = country['states']
        state = list(filter(lambda s: s['stateFipsCode'] == state_code, state_list))[0]
        huc_list = state['hydrologicUnitCodes']
    except IndexError:
        huc_list = []
    return huc_list


def get_mcds(country_code, state_code):
    try:
        mcd_file = open(os.path.join(PROJECT_DIR, 'references/mcd.json'))
        with mcd_file:
            mcd = json.loads(mcd_file.read())
        country_list = mcd['countries']
        country = list(filter(lambda c: c['countryCode'] == country_code, country_list))[0]
        state_list = country['states']
        state = list(filter(lambda s: s['stateFipsCode'] == state_code, state_list))[0]
        mcd_list = state['minorCivilDivisionCodes']
    except IndexError:
        mcd_list = []
    return mcd_list


def get_national_aquifers(country_code, state_code):
    try:
        national_aquifer_file = open(os.path.join(PROJECT_DIR, 'references/national_aquifer.json'))
        with national_aquifer_file:
            national_aquifer = json.loads(national_aquifer_file.read())
        country_list = national_aquifer['countries']
        country = list(filter(lambda c: c['countryCode'] == country_code, country_list))[0]
        state_list = country['states']
        state = list(filter(lambda s: s['stateFipsCode'] == state_code, state_list))[0]
        national_aquifer_list = state['nationalAquiferCodes']
    except IndexError:
        national_aquifer_list = []
    return national_aquifer_list


def get_national_water_use_codes(site_type_code):
    try:
        national_water_use_file = open(os.path.join(PROJECT_DIR, 'references/national_water_use.json'))
        with national_water_use_file:
            national_water_use = json.loads(national_water_use_file.read())
        site_type_list = national_water_use['siteTypeCodes']
        site_type = list(filter(lambda st: st['siteTypeCode'] == site_type_code, site_type_list))[0]
        national_water_use_code_list = site_type['nationalWaterUseCodes']
    except IndexError:
        national_water_use_code_list = []
    return national_water_use_code_list


reference_lists_file = open(os.path.join(PROJECT_DIR, 'references/reference_lists.json'))
with reference_lists_file:
    reference_lists = json.loads(reference_lists_file.read())

site_type_transition_file = open(os.path.join(PROJECT_DIR, 'references/site_type_transition.json'))
with site_type_transition_file:
    site_type_transition = json.loads(site_type_transition_file.read())

state_file = open(os.path.join(PROJECT_DIR, 'references/state.json'))
with state_file:
    state_json = json.loads(state_file.read())


def get_state_codes(country_code):
    try:
        country_list = state_json['countries']
        country = list(filter(lambda c: c['countryCode'] == country_code, country_list))[0]
        state_list = country['states']
        state_code_list = [d['stateFipsCode'] for d in state_list]
    except IndexError:
        state_code_list = []
    return state_code_list


def get_state_attributes(country_code, state_code):
    try:
        country_list = state_json['countries']
        country = list(filter(lambda c: c['countryCode'] == country_code, country_list))[0]
        state_list = country['states']
        state_attributes = list(filter(lambda s: s['stateFipsCode'] == state_code, state_list))[0]
    except IndexError:
        state_attributes = {}
    return state_attributes
