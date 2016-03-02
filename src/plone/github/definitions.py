# -*- coding: utf-8 -*-
import json


def load_definitions(filepath):
    with open(filepath, 'r') as fd:
        defs = json.load(fd)

    # make all tuples and expand !tag
    for key in defs['MIGRATIONS']:
        value = defs['MIGRATIONS'][key]
        if isinstance(value, list):
            defs['MIGRATIONS'][key] = tuple(value)
        if not isinstance(value, tuple):
            defs['MIGRATIONS'][key] = (value,)
    return defs
