
import os
import yaml
from cerberus import schema_registry

PROJECT_DIR = os.path.dirname(__file__)

fd = open(os.path.join(PROJECT_DIR, 'schema.yml'))
with fd:
    insert_schema = yaml.load(fd.read())

fdw = open(os.path.join(PROJECT_DIR, 'warning_schema.yml'))
with fdw:
    warning_schema = yaml.load(fdw.read())

schema_registry.add('error_schema', insert_schema)
schema_registry.add('warning_schema', warning_schema)


def get_insert_schema():

    return insert_schema


def get_warning_schema():

    return warning_schema
