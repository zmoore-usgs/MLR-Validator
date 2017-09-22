
import os
import sys
import yaml

PROJECT_DIR = os.path.dirname(__file__)
EXEC_PREFIX = sys.exec_prefix

fd = open(os.path.join(PROJECT_DIR, 'data/schema.yml'))
with fd:
    insert_schema = yaml.load(fd.read())


def get_insert_schema():

    return insert_schema
