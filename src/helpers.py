import json
import sys

def is_in_list(l, v):
    if l is None:
        return False
    return v in l

def get_value(d, key, default = None):
    if d is None or key not in d:
        return default
    return d[key]

def parse_int(val, default = -1):
    try:
        return int(val)
    except TypeError:
        return default
    except ValueError:
        return default

def parse_float(val, default = -1.0):
    try:
        return float(val)
    except TypeError:
        return default
    except ValueError:
        return default

def parse_json(json_str, default = None):
    try:
        return json.loads(json_str)
    except ValueError:
        return default

def get_path_id(path):
    if path is None:
        return ''
    path_list = path.split('/')
    return path_list[-1]

def flatten(*lists):
    ret = list()
    for l in lists:
        for item in l:
            ret.append(item)
    return ret
