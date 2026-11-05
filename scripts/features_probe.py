"""Which native GitHub features the organization already uses.

Writes data/features_in_use.json. All searches are restricted to public
repositories.
"""
import base64
import json
import re

from scripts.common import DATA
from scripts.gh_graphql import gql, rest

CORE_REPOS = ["volto", "aurora", "Products.CMFPlone", "plone.restapi", "documentation", "mockup"]
PUB = "org:plone is:public"

QUERY = """{
  types: repository(owner: "plone", name: "volto") { issueTypes(first: 25) { nodes { name isEnabled } } }
  %s
  typed_open: search(type: ISSUE, query: "%s is:issue is:open type:Bug,Feature,Task,PLIP") { issueCount }
  typed_recent: search(type: ISSUE, query: "%s is:issue created:>=2025-06-01 type:Bug,Feature,Task,PLIP") { issueCount }
  all_recent: search(type: ISSUE, query: "%s is:issue created:>=2025-06-01") { issueCount }
  drafts: search(type: ISSUE, query: "%s is:pr is:open draft:true") { issueCount }
  automerge: search(type: ISSUE, query: "%s is:pr is:open auto-merge:true") { issueCount }
  regressions: search(type: ISSUE, query: "%s is:issue is:open label:\\"02 type: regression\\"") { issueCount }
  gfi: search(type: ISSUE, query: "%s is:issue is:open label:\\"good first issue\\"") { issueCount }
  hw: search(type: ISSUE, query: "%s is:issue is:open label:\\"help wanted\\"") { issueCount }
}"""


def main() -> None:
    repo_parts = " ".join(
        f'r{i}: repository(owner: "plone", name: "{name}") {{ hasDiscussionsEnabled }}'
        for i, name in enumerate(CORE_REPOS))
    data = gql(QUERY % ((repo_parts,) + (PUB,) * 8))
    fields = rest("orgs/plone/issue-fields")
    cfg = rest("repos/plone/.github/contents/.github/ISSUE_TEMPLATE/config.yml")
    config_yml = base64.b64decode(cfg["content"]).decode()
    blank = re.search(r"^blank_issues_enabled:\s*(\w+)", config_yml, re.M)
    out = {
        "issue_types": [t["name"] for t in data["types"]["issueTypes"]["nodes"] if t["isEnabled"]],
        "typed_open_issues": data["typed_open"]["issueCount"],
        "typed_since_2025_06": data["typed_recent"]["issueCount"],
        "issues_since_2025_06": data["all_recent"]["issueCount"],
        "discussions_enabled": {name: data[f"r{i}"]["hasDiscussionsEnabled"] for i, name in enumerate(CORE_REPOS)},
        "open_draft_prs": data["drafts"]["issueCount"],
        "open_automerge_prs": data["automerge"]["issueCount"],
        "open_regressions": data["regressions"]["issueCount"],
        "open_good_first_issue_exact": data["gfi"]["issueCount"],
        "open_help_wanted_exact": data["hw"]["issueCount"],
        "issue_fields": [{"name": f["name"], "visibility": f["visibility"]} for f in fields],
        "blank_issues_enabled": (blank.group(1).lower() == "true") if blank else None,
    }
    (DATA / "features_in_use.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
