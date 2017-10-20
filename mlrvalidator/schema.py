
import os
import sys
import yaml

PROJECT_DIR = os.path.dirname(__file__)

fd = open(os.path.join(PROJECT_DIR, 'schemas/reference_validation_schema.yml'))
with fd:
    reference_schema = yaml.load(fd.read())

fd = open(os.path.join(PROJECT_DIR, 'schemas/single_field_validation_schema.yml'))
with fd:
    single_field_schema = yaml.load(fd.read())

fd = open(os.path.join(PROJECT_DIR, 'schemas/cross_field_schema.yml'))
with fd:
    cross_field_schema = yaml.load(fd.read())

fdw = open(os.path.join(PROJECT_DIR, 'schemas/warning_schema.yml'))
with fdw:
    warning_schema = yaml.load(fdw.read())

fd = open(os.path.join(PROJECT_DIR, 'schemas/site_type_cross_field_schema.yml'))
with fd:
    site_type_cross_field_schema = yaml.load(fd.read())
