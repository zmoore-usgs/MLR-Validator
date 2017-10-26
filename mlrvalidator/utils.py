
def get_dict(dictlist, parent_key, parent_value):
    '''
    :param dictlist: list of dictionaries
    Assumes dictlist has this form: [{'a': 'A', 'b' : [{'c' : 'C1'}, {'c' : 'C2'}]}, {'a': 'A1', 'b' : [{'c' : 'C3'}]}]
    :param string reference_key: the key of the information that we want this method to return. In above could use 'b'
    :param parent_key:  the key of the dictionary key to use to match parent_value. In above example could use 'a'
    :param parent_value: the value of parent_key to find. In above example could use 'A'
    :return: dictionary that is found by using parent_key and parent_value to find the dictionary in dictlist. Will
        return the first one found.
    '''
    try:
        result = list(filter(lambda c: c[parent_key] == parent_value, dictlist))[0]
    except (IndexError, KeyError):

        result = {}

    return result


