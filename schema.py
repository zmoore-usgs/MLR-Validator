
import os
import yaml

PROJECT_DIR = os.path.dirname(__file__)

fd = open(os.path.join(PROJECT_DIR, 'schema.yml'))
with fd:
    insert_schema = yaml.load(fd.read())


def get_insert_schema():

    return insert_schema
