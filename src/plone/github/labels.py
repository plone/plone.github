# -*- coding: utf-8 -*-
"""
This script manages labels for all repositories of an organization.
"""
from __future__ import print_function
from definitions import CFG
from github import Github
from github.GithubException import GithubException

import argparse
import re


# the following map defines labels valid for the whole organization.
# they will be added to every repository, color will be set (also updated)
# GENERAL_LABELS = {
#    Pull Request Specific Labels
#    'pr wip': '0052cc',
# }


# special labels are labels specific to one or more repositories, but they
# wont be added to all. This way we can change its color.
# SPECIAL_LABELS = {

#     # 'plog2014': 'f7f7f7',
# }

# Migration of labels. This updates name and color (taken from ALL_LABELS)
# At the moment it fails if the target label already exists.
# MIGRATIONS = {
#     'Question': 'question',
# }

# rough validation
# assert(
#     not set(['GENERAL_LABELS'].keys()) & set(CFG['SPECIAL_LABELS'].keys()),
#     'general and special labels must not overlap'
# )
# for simplification of color picking
ALL_LABELS = dict(
    CFG['GENERAL_LABELS'].items() + CFG['SPECIAL_LABELS'].items()
)

# define command line arguments
argparser = argparse.ArgumentParser()
argparser.add_argument(
    '--token',
    required=True,
    help='Github token',
)
argparser.add_argument(
    '--summary',
    help='Show summary of labels with used repos and colors',
    action='store_true'
)
argparser.add_argument(
    '--debug-limit',
    type=int,
    help='Limit the number of repos fetched, for debugging'
)
argparser.add_argument(
    'repos',
    default=[],
    nargs='*',
    help='Repositories to match'
)


def _migrate_label(repo, label, current_label_names, all_labels):
    """Either renames a label or if already exist it set the target on
    all issues and deletes the old label

    - given label is a valid key of MIGRATE
    """
    label_name = label.name  # may chnage otherwise while migration
    for new_label in CFG['MIGRATIONS'][label_name]:
        if new_label in current_label_names:
            # ok, target exists, so we have to fetch with this label
            # and give it the new label, then delete the old label

            # set new label to all issues with old label
            print(
                '-> migration for {0}" but target {1} exists, rename'
                'and remove old label'.format(
                    label.name,
                    CFG['MIGRATIONS'][label_name]
                )
            )
            for issue in repo.get_issues(state='all', labels=[label]):
                issue.set_labels(
                    *[_.name for _ in issue.labels if _ != label] +
                    [new_label]
                )
            current_label_names.remove(label_name)
            label.delete()
            continue
        print(
            '-> migrate {0} to {1}'.format(
                label_name,
                CFG['MIGRATIONS'][label_name]
            )
        )
        current_label_names.append(new_label)
        all_labels.update(new_label)
        try:
            label.edit(
                new_label,
                ALL_LABELS.get(
                    CFG['MIGRATIONS'][label_name],
                    CFG['FALLBACKCOLOR']
                )
            )
        except:
            print('   failed... :(')
        label.update()


def _handle_milstones(repo):
    # milestones
    current_milestones = set()
    for ms in repo.get_milestones():
        current_milestones.update([ms.title.lower()])
    for new_milestone in CFG['MILESTONES']:
        if new_milestone.lower() not in current_milestones:
            print('-> create milestone: "{0}"'.format(new_milestone))
            try:
                repo.create_milestone(title=new_milestone)
            except GithubException:
                # XXX
                print('   milestone closed')


def _show_summary(label_summary):
    print('-' * 47)
    print('Overall label summary with colors')
    print('-' * 47)
    for label_name, label_repo_colors in sorted(label_summary.items()):
        print('\n[{0}]'.format(label_name))
        for repo, color in sorted(label_repo_colors.items()):
            r, g, b = [int(_, 16) for _ in re.findall('..', color)]
            print(repo.ljust(40, '.'), color)


def manage_labels():
    args = argparser.parse_args()
    gh = Github(args.token)
    organization = gh.get_organization(CFG['ORGANIZATION'])
    all_labels = set()
    label_summary = {}
    skipped = []
    for idx, repo in enumerate(organization.get_repos()):
        if (
            (args.repos and repo.name not in args.repos) or
            repo.name not in CFG['REPOSITORIES']
        ):
            skipped.append(repo.name)
            print(
                'skip #{0} {1} (limit at {2} of {3})'.format(
                    idx+1,
                    repo.name,
                    gh.rate_limiting[0],
                    gh.rate_limiting[1]
                )
            )
            continue
        if args.debug_limit and idx+1 > args.debug_limit:
            break
        print(
            'repo #{0} {1} (limit at {2} of {3})'.format(
                idx+1,
                repo.name,
                gh.rate_limiting[0],
                gh.rate_limiting[1]
            )
        )

        _handle_milstones(repo)

        # labels
        current_labels = [_ for _ in repo.get_labels()]
        current_label_names = [_.name for _ in current_labels]
        all_labels.update(current_label_names)
        for clabel in current_labels:
            # collect summary
            if clabel.name not in label_summary:
                label_summary[clabel.name] = {}
            label_summary[clabel.name][repo.name] = clabel.color

            # migrate name
            if clabel.name in CFG['MIGRATIONS']:
                _migrate_label(repo, clabel, current_label_names, all_labels)

            # adjust color
            if clabel.name in ALL_LABELS \
               and clabel.color != ALL_LABELS[clabel.name]:
                print(
                    '-> update color of "{0}" to "{1}"'.format(
                        clabel.name,
                        ALL_LABELS[clabel.name]
                    )
                )
                clabel.edit(clabel.name, ALL_LABELS[clabel.name])

        # deal general labels: create missing
        for label_name, color in sorted(CFG['GENERAL_LABELS'].items()):
            if label_name in current_label_names:
                continue
            print('-> create label {0}'.format(label_name))
            repo.create_label(label_name, color)
    print("skipped: {0}".format(', '.join(sorted(skipped))))

    if args.summary:
        _show_summary(label_summary)
