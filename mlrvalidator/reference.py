import os
import sys

PROJECT_DIR = os.path.dirname(__file__)
EXEC_PREFIX = sys.exec_prefix

fd = open(os.path.join(PROJECT_DIR, 'references/agency.txt'))
with fd:
    agency = fd.read()