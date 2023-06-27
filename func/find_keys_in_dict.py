import json


def find_keys_in_dict(dictionary, keys_to_find):
    result = []
    for key, value in dictionary.items():
        if key in keys_to_find:
            result.append({key: value})
        if isinstance(value, dict):
            result.extend(find_keys_in_dict(value, keys_to_find))
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    result.extend(find_keys_in_dict(item, keys_to_find))
    return result
