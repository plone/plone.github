"""Public organization project boards: fields, views and filters, plus item
samples of the key boards. Private boards and items from private
repositories are left out.

Writes data/projects.json and data/projects_items_sample.json.
"""
import json
from collections import Counter

from scripts.common import DATA, load_repos
from scripts.gh_graphql import gql

KEY_BOARDS = [12, 19, 28, 33, 34, 47, 55, 58, 66, 72, 76, 93]

PROJECTS_QUERY = """
query($cursor: String) {
  organization(login: "plone") {
    projectsV2(first: 20, after: $cursor, orderBy: {field: UPDATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title url closed public updatedAt createdAt
        items { totalCount }
        fields(first: 40) { nodes {
          ... on ProjectV2Field { name dataType }
          ... on ProjectV2SingleSelectField { name dataType options { name } }
          ... on ProjectV2IterationField { name dataType }
        } }
        views(first: 30) { nodes { name layout filter
          groupByFields(first: 5) { nodes { ... on ProjectV2Field { name } ... on ProjectV2SingleSelectField { name } ... on ProjectV2IterationField { name } } }
          verticalGroupByFields(first: 5) { nodes { ... on ProjectV2Field { name } ... on ProjectV2SingleSelectField { name } ... on ProjectV2IterationField { name } } }
        } }
      }
    }
  }
}"""

ITEMS_QUERY = """
query($n: Int!) { organization(login: "plone") { projectV2(number: $n) {
  items(first: 100) { totalCount nodes {
    type
    status: fieldValueByName(name: "Status") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
    prio: fieldValueByName(name: "Priority") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
    content {
      ... on Issue { state repository { name } issueType { name } labels(first: 20) { nodes { name } } }
      ... on PullRequest { state repository { name } labels(first: 20) { nodes { name } } }
      ... on DraftIssue { title }
    } } } } } }"""


def fetch_projects() -> list[dict]:
    projects, cursor = [], None
    while True:
        page = gql(PROJECTS_QUERY, cursor=cursor)["organization"]["projectsV2"]
        projects += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            return projects
        cursor = page["pageInfo"]["endCursor"]


def sample(number: int, public_repos: set[str]) -> dict:
    items = gql(ITEMS_QUERY, n=number)["organization"]["projectV2"]["items"]
    nodes = items["nodes"]
    kept = [i for i in nodes if ((i["content"] or {}).get("repository") or {}).get("name") in public_repos]
    repos = Counter(i["content"]["repository"]["name"] for i in kept)
    labels = Counter(l["name"] for i in kept for l in (i["content"].get("labels") or {}).get("nodes", []))
    return {
        "total": items["totalCount"], "sampled": len(nodes), "from_public_repos": len(kept),
        "open": sum(1 for i in kept if i["content"].get("state") == "OPEN"),
        "issue_typed": sum(1 for i in kept if i["content"].get("issueType")),
        "repos": repos.most_common(8),
        "status": Counter((i["status"] or {}).get("name") for i in kept).most_common(8),
        "priority": Counter((i["prio"] or {}).get("name") for i in kept).most_common(4),
        "labels": labels.most_common(12),
    }


def main() -> None:
    public_repos = {r["name"] for r in load_repos()}
    projects = fetch_projects()
    public = [p for p in projects if p["public"]]
    (DATA / "projects.json").write_text(json.dumps(
        {"total_boards": len(projects), "private_boards_omitted": len(projects) - len(public), "boards": public},
        indent=1) + "\n")
    samples = {}
    for p in public:
        if p["number"] in KEY_BOARDS:
            samples[str(p["number"])] = {"title": p["title"], **sample(p["number"], public_repos)}
    (DATA / "projects_items_sample.json").write_text(json.dumps(samples, indent=1) + "\n")
    print(f"{len(public)} public boards of {len(projects)}; sampled {len(samples)} key boards")


if __name__ == "__main__":
    main()
