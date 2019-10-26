# -*- coding: utf-8 -*-
"""
This script manages labels for all repositories of an organization.
"""
from __future__ import print_function
from definitions import load_definitions
from github import Github
from github.GithubException import GithubException

import argparse
import re

# define command line arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-t", "--token", required=True, help="Github token")
argparser.add_argument(
    "-c",
    "--configuration",
    default="definitions.json",
    help="configuration file (json) to be used.",
)
argparser.add_argument(
    "-s",
    "--summary",
    help="Show summary of labels with used repos and colors",
    action="store_true",
)
argparser.add_argument(
    "--debug-limit", type=int, help="Limit the number of repos fetched, for debugging"
)
argparser.add_argument("repos", default=[], nargs="*", help="Repositories to match")


def _migrate_label(cfg, repo, label, current_label_names, new_labels):
    """Either renames a label or if already exist it set the target on
    all issues and deletes the old label

    - given label is a valid key of MIGRATE
    """
    old_label = label.name  # may chnage otherwise while migration
    for new_label in cfg["MIGRATIONS"][old_label]:
        if new_label in current_label_names:
            # ok, target exists, so we have to fetch with this label
            # and give it the new label, then delete the old label

            # set new label to all issues with old label
            print(
                '-> migration for {0}" but target {1} exists, rename'
                "and remove old label".format(label.name, cfg["MIGRATIONS"][old_label])
            )
            for issue in repo.get_issues(state="all", labels=[label]):
                issue.set_labels(
                    *[_.name for _ in issue.labels if _ != label] + [new_label]
                )
            current_label_names.remove(old_label)
            label.delete()
            continue
        print("-> migrate {0} to {1}".format(old_label, cfg["MIGRATIONS"][old_label]))
        current_label_names.append(new_label)
        new_labels.update(new_label)
        try:
            label.edit(
                new_label,
                cfg["LABELS"].get(cfg["MIGRATIONS"][old_label], cfg["FALLBACKCOLOR"]),
            )
        except Exception:
            print("   failed... :(")
        label.update()


def _handle_milstones(cfg, repo):
    # milestones
    current_milestones = set()
    for ms in repo.get_milestones():
        current_milestones.update([ms.title.lower()])
    for new_milestone in cfg["MILESTONES"]:
        if new_milestone.lower() not in current_milestones:
            print('-> create milestone: "{0}"'.format(new_milestone))
            try:
                repo.create_milestone(title=new_milestone)
            except GithubException:
                # XXX
                print("   milestone already closed, do nothing")


def _show_summary(label_summary):
    print("-" * 47)
    print("Overall label summary with colors")
    print("-" * 47)
    for label_name, label_repo_colors in sorted(label_summary.items()):
        print("\n[{0}]".format(label_name))
        for repo, color in sorted(label_repo_colors.items()):
            r, g, b = [int(_, 16) for _ in re.findall("..", color)]
            print(repo.ljust(40, "."), color)


def manage_labels():  # NOQA: C901
    args = argparser.parse_args()
    cfg = load_definitions(args.configuration)
    gh = Github(args.token)
    all_labels = set()
    label_summary = {}
    skipped = []
    for organisation in cfg["ORGANIZATIONS"]:
        repositories = cfg["ORGANIZATIONS"][organisation]
        gh_organization = gh.get_organization(organisation)
        for idx, repo in enumerate(gh_organization.get_repos()):
            if (
                args.repos and repo.name not in args.repos
            ) or repo.name not in repositories:
                skipped.append(repo.name)
                if repo.name not in repositories:
                    reason = "by cfg"
                else:
                    reason = "by arg"
                print(
                    "skip #{0} {1} {2} (limit at {3} of {4})".format(
                        idx + 1,
                        reason,
                        repo.name,
                        gh.rate_limiting[0],
                        gh.rate_limiting[1],
                    )
                )
                continue
            if args.debug_limit and idx + 1 > args.debug_limit:
                break
            print(
                "repo #{0} {1} (limit at {2} of {3})".format(
                    idx + 1, repo.name, gh.rate_limiting[0], gh.rate_limiting[1]
                )
            )

            _handle_milstones(cfg, repo)

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
                if clabel.name in cfg["MIGRATIONS"]:
                    _migrate_label(cfg, repo, clabel, current_label_names, all_labels)

                # adjust color
                if (
                    clabel.name in cfg["LABELS"]
                    and clabel.color != cfg["LABELS"][clabel.name]
                ):
                    print(
                        '-> update color of "{0}" to "{1}"'.format(
                            clabel.name, cfg["LABELS"][clabel.name]
                        )
                    )
                    clabel.edit(clabel.name, cfg["LABELS"][clabel.name])

            # create missing
            for label_name, color in sorted(cfg["LABELS"].items()):
                if label_name in current_label_names:
                    continue
                print("-> create label {0}".format(label_name))
                repo.create_label(label_name, color)

    print("skipped: {0}".format(", ".join(sorted(skipped))))

    if args.summary:
        _show_summary(label_summary)
