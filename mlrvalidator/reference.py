import os
import json

PROJECT_DIR = os.path.dirname(__file__)

agency_file = open(os.path.join(PROJECT_DIR, 'references/agency.json'))
with agency_file:
    agency = json.loads(agency_file.read())

state_file = open(os.path.join(PROJECT_DIR, 'references/state.json'))
with state_file:
    state = json.loads(state_file.read())

mcd_file = open(os.path.join(PROJECT_DIR, 'references/mcd.json'))
with mcd_file:
    mcd = json.loads(mcd_file.read())
