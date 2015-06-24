# -*- coding: utf-8 -*-

MILESTONES = {
    'Plone 4.3',
    'Plone 5.0',
    'Plone 5.1',
}

GENERAL_LABELS = {
    '01 type: bug': 'f70000',
    '02 type: regression': 'f39100',
    '03 type: feature': '00c000',
    '04 type: enhancement': 'f3f300',
    '05 type: question': 'de00ed',
    '11 prio: blocker': '990000',
    '12 prio: high': 'cc0000',
    '13 prio: normal':  'e06666',
    '14 prio: low': 'f4cccc',
    '21 status: confirmed':  'd9ead3',
    '22 status: in-progress': 'b6d7a8',
    '23 status: needs help': '93c47d',
    '24 status: needs rebase': '93c47d',
    '25 status: needs docs': '93c47d',
    '26 status: needs review': '93c47d',
    '27 status: testing': '6aa84f',
    '28 status: ready':  '38761d',
    '29 status: deferred':  '274e13',
    '31 status: duplicate':  '666666',
    '32 status: wontfix': '434343',
    '33 status: invalid': '000000',
    '41 lvl: easy': 'a4c2f4',
    '42 lvl: moderate': '3c78d8',
    '43 lvl: complex':  '1c4587',
}

FALLBACKCOLOR = 'f3f3f3'

SPECIAL_LABELS = {}

MIGRATIONS = {
    '1.x': '!tag',
    '2.x': '!tag',
    '3.x': '!tag',
    '4.3': '!tag',
    '5.0': '!tag',
    'Accessibility': 'tag: accessibility',
    'Ansible': 'tag: ansible',
    'area:accessibility': 'tag: accessibility',
    'area:documentation': 'tag: documentation',
    'area:plone.app.widgets': 'tag: plone.app.widgets',
    'area:plone5': '@Plone 5.0',
    'area:styles': 'tag: styles',
    'Bug': '01 type: bug',
    'bug': '01 type: bug',
    'bundle:barceloneta': 'tag: bundle barceloneta',
    'bundle:foldercontents': '!tag',
    'bundle:toolbar': '!tag',
    'bundle:widgets': '!tag',
    'ci': '!tag',
    'Cleanup needed': ('!tag', '23 status: needs help'),
    'Confirmed': '21 status: confirmed',
    'Content': '!tag',
    'Contributor profile': '!tag',
    'Dependencies': '!tag',
    'Design': '!tag',
    'developer': '!tag',
    'Difficulty-Easy': '41 lvl: easy',
    'Difficulty-Hard': '43 lvl: complex',
    'Difficulty-Moderate': '42 lvl: moderate',
    'documentation': '!tag',
    'duplicate': '31 status: duplicate',
    'Enhancement': '04 type: enhancement',
    'enhancement': '04 type: enhancement',
    'Feature': '03 type: feature',
    'feature': '03 type: feature',
    'feature request': '03 type: feature',
    'Foundation Information': '!tag',
    'help wanted': '23 status: needs help',
    'HomePage': '!tag',
    'hosting': '!tag',
    'Important': '12 prio: high',
    'important': '12 prio: high',
    'imported': '!tag',
    'imported from dev.plone.org': '!tag',
    'in progress': '22 status: in-progress',
    'invalid': '33 status: invalid',
    'Jenkins Job Builder': '!tag',
    'Jenkins VM donation': '!tag',
    'migration': '!tag',
    'missing': '!tag',
    'Missing': '!tag',
    'needs review': '26 status: needs review',
    'OSX': '!tag',
    'pattern:filemanager': '!tag',
    'pattern:modal': '!tag',
    'pattern:pickadate': '!tag',
    'pattern:querystring': '!tag',
    'pattern:relateditems': '!tag',
    'pattern:resourceregistry': '!tag',
    'pattern:select2': '!tag',
    'pattern:structure': '!tag',
    'pattern:thememapper': '!tag',
    'PLIP': ('03 type: feature', 'tag: PLIP'),
    'PLIP 10359: z3cform control panel':
        ('03 type: feature', 'tag: PLIP 10359: z3cform control panel'),
    'PLIP 13260: Remove CMF':
        ('03 type: feature', 'tag: PLIP 13260: Remove CMF'),
    'PLIP 13350: Edit Member Schema TTW':
        ('03 type: feature', 'tag: PLIP 13350: Edit Member Schema TTW'),
    'PLIP 13770: Portal Tools Removal':
        ('03 type: feature', 'tag: PLIP 13770: Portal Tools Removal'),
    'PLIP 13787 - Barceloneta / MainTemplate':
        ('03 type: feature', 'tag: PLIP 13787 - Barceloneta / MainTemplate'),
    'plog2014': '!tag',
    'plone.app.blocks': '!tag',
    'plone.app.standardtiles': '!tag',
    'plone.app.tiles': '!tag',
    'plone.tiles': '!tag',
    'plone3': '!tag',
    'plone4': '!tag',
    'plone5': '!tag',
    'pr 3.3': 'tag: Plone 3.3',
    'pr ok': '28 status: ready',
    'pr orphaned': '23 status: needs help',
    'pr p4.3': '@plone 4.3',
    'pr p5.0': '@plone 5.0',
    'pr ready': '28 status: ready',
    'pr rebase': '24 status: needs rebase',
    'pr review': '26 status: needs review',
    'pr testing': '27 status: testing',
    'pr wip': '22 status: in-progress',
    'prio:high': '12 prio: high',
    'prio:low': '14 prio: low',
    'prio:normal': '13 prio: normal',
    'Priority-High': '12 prio: high',
    'Priority-Low': '14 prio: low',
    'Priority-Medium': '13 prio: normal',
    'ready': '28 status: ready',
    'regression': '02 type: regression',
    'Regression': '02 type: regression',
    'regression from atct': ('02 type: regression', 'tag: from atct'),
    'release': 'tag: release',
    'request for comments': '26 status: needs review',
    'skunkworks': '!tag',
    'sprint': 'tag: sprint',
    'Sprint': 'tag: sprint',
    'status:confirmed': '21 status: confirmed',
    'status:deferred': '29 status: deferred',
    'status:feedback-needed': '26 status: needs review',
    'status:fix-committed': '28 status: ready',
    'status:in-progress': '22 status: in-progress',
    'status:rejected': '33 status: invalid',
    'status:resolved': '28 status: ready',
    'styleguide': '!tag',
    'Testing': '27 status: testing',
    'testing': '27 status: testing',
    'Tests': '!tag',
    'Theme': '!tag',
    'todo': '04 type: enhancement',
    'toolbar': '!tag',
    'Type-Documentation': '25 status: needs docs',
    'type:bug': '01 type: bug',
    'type:feature': '03 type: feature',
    'type:invalid': '33 status: invalid',
    'unconfirmed': '26 status: needs review',
    'UX Editor': '!tag',
    'UX Integrator/Themer': '!tag',
    'UX Site Admin': '!tag',
    'widgets': '!tag',
    'wineandbeersprint': '!tag',
    'wontfix': '32 status: wontfix',
}

# make all tuples and expand !tag
for key in MIGRATIONS:
    value = MIGRATIONS[key]
    if not isinstance(value, tuple):
        value = (value,)
    expanded = []
    for entry in value:
        if entry == '!tag':
            expanded.append('90 tag: {0}'.format(key))
        elif entry in GENERAL_LABELS:
            expanded.append(entry)
        elif entry.startswith('tag: '):
            expanded.append('90 ' + entry)
        elif entry.startswith('@'):
            # handle milestones
            pass
        else:
            raise ValueError((key, entry))
    MIGRATIONS[key] = tuple(expanded)
