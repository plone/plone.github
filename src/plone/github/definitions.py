# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import json
import os

BASEDIR = os.path.dirname(__file__)
with open(os.path.join(BASEDIR, 'definitions.json'), 'r') as fd:
    CFG = json.load(fd)

# make all tuples and expand !tag
for key in CFG['MIGRATIONS']:
    value = CFG['MIGRATIONS'][key]
    if isinstance(value, list):
        value = tuple(value)
    if not isinstance(value, tuple):
        value = (value,)
    expanded = []
    for entry in value:
        if entry == '!tag':
            expanded.append('tag: {0}'.format(key))
        elif entry.startswith('tag: '):
            expanded.append('99 ' + entry)
        elif entry.startswith('99 tag: '):
            expanded.append(entry)
        elif entry.startswith('@'):
            # handle milestones
            pass
        elif entry in CFG['GENERAL_LABELS']:
            expanded.append(entry)
        else:
            raise ValueError((key, entry))
    CFG['MIGRATIONS'][key] = tuple(expanded)
