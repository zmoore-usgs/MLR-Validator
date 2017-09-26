import os
import sys
import json

PROJECT_DIR = os.path.dirname(__file__)
EXEC_PREFIX = sys.exec_prefix

agency_file = open(os.path.join(PROJECT_DIR, 'references/agency.txt'))
with agency_file:
    agency = set(line.strip() for line in agency_file)

state_file = open(os.path.join(PROJECT_DIR, 'references/state.json'))
with state_file:
    state = json.loads(state_file.read())

mcd_file = open(os.path.join(PROJECT_DIR, 'references/mcd.json'))
with mcd_file:
    mcd = json.loads(mcd_file.read())
