
def filter_dict(dictionary:dict, filters:list):
    results = {}
    for filter in filters:
        results.update({filter : dictionary[filter]})
    return results


