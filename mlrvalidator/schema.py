
import os
import sys
import yaml
from cerberus import schema_registry

PROJECT_DIR = os.path.dirname(__file__)
EXEC_PREFIX = sys.exec_prefix

fd = open(os.path.join(PROJECT_DIR, 'data/schema.yml'))
with fd:
    insert_schema = yaml.load(fd.read())

fdw = open(os.path.join(PROJECT_DIR, 'data/warning_schema.yml'))
with fdw:
    warning_schema = yaml.load(fdw.read())

schema_registry.add('insert_error_schema', insert_schema)
schema_registry.add('insert_warning_schema', warning_schema)
