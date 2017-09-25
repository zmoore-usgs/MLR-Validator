
import os
import sys
import yaml

PROJECT_DIR = os.path.dirname(__file__)
EXEC_PREFIX = sys.exec_prefix

fd = open(os.path.join(PROJECT_DIR, 'schemas/error_schema.yml'))
with fd:
    error_schema = yaml.load(fd.read())

fdw = open(os.path.join(PROJECT_DIR, 'schemas/warning_schema.yml'))
with fdw:
    warning_schema = yaml.load(fdw.read())
