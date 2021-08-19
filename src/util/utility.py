
def filter_dict(dictionary:dict, filters:list):
    '''Filters the dictionary and returns a new dictionary based on the filterd keys'''
    results = {}
    for filter in filters:
        results.update({filter : dictionary[filter]})
    return results

def format_dict_to_text(dictionary:dict, filters= None):
    '''Returns a readable formatted text containing the elements of the dictionary.
    You can also filter the results in the dictionary by asigning the filters variable.
    Make sure that all the keys in the dictionary are strings or have a proper string representation.'''

    if filters:
        dictionary = filter_dict(dictionary, filters)
    result = ''
    for key, value in dictionary.items():
        result += f"   - {str(key).title()}: {value}\n"
    return result
    
    


