
from unittest import TestCase

from ..utils import get_dict

class GetDictTestCase(TestCase):

    def test_empty_dictlist(self):
        self.assertEqual(get_dict([], 'a', 'A'), {})

    def test_parent_key_in_list_but_not_value(self):
        self.assertEqual(get_dict([{
            'a': 'A',
            'b': 1
        },{
            'a': 'B',
            'b': 2
        }], 'a', 'C'), {})

    def test_parent_key_in_list_with_value(self):
        self.assertEqual(get_dict([{
            'a': 'A',
            'b': 1
        }, {
            'a': 'B',
            'b': 2
        }], 'a', 'A'), {'a': 'A', 'b': 1})

    def test_missing_parent_key_in_list(self):
        self.assertEqual(get_dict([{
            'a': 'A',
            'b': 1
        }, {
            'a': 'B',
            'b': 2
        }], 'c', 'C'), {})
