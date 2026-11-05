"""Fetch every label of every *public* repository in the plone org.

Writes data/plone_labels.json: a list of
{"name", "archived", "fork", "visibility": "public", "createdAt", "labels": [...]}.
"""
import json
from datetime import datetime, timezone
from typing import Iterator

from scripts.common import DATA
from scripts.gh_graphql import gql, is_public

REPOS_QUERY = """
query($cursor: String) {
  organization(login: "plone") {
    repositories(first: 25, after: $cursor, orderBy: {field: NAME, direction: ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name isPrivate isArchived isFork createdAt
        labels(first: 100) {
          pageInfo { hasNextPage endCursor }
          nodes { name description color }
        }
      }
    }
  }
}"""

LABELS_QUERY = """
query($name: String!, $cursor: String) {
  repository(owner: "plone", name: $name) {
    labels(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { name description color }
    }
  }
}"""


def fetch_pages() -> Iterator[dict]:
    """Yield one ``repositories`` connection page after another."""
    cursor = None
    while True:
        page = gql(REPOS_QUERY, cursor=cursor)["organization"]["repositories"]
        yield page
        if not page["pageInfo"]["hasNextPage"]:
            return
        cursor = page["pageInfo"]["endCursor"]


def collect() -> list[dict]:
    """Public repositories with their complete label lists."""
    repos = []
    for page in fetch_pages():
        for repo in page["nodes"]:
            if not is_public(repo):
                continue
            labels = list(repo["labels"]["nodes"])
            info = repo["labels"]["pageInfo"]
            while info["hasNextPage"]:
                more = gql(LABELS_QUERY, name=repo["name"], cursor=info["endCursor"])["repository"]["labels"]
                labels += more["nodes"]
                info = more["pageInfo"]
            repos.append({
                "name": repo["name"], "archived": repo["isArchived"], "fork": repo["isFork"],
                "visibility": "public", "createdAt": repo["createdAt"], "labels": labels,
            })
    return repos


def main() -> None:
    repos = collect()
    DATA.mkdir(exist_ok=True)
    (DATA / "plone_labels.json").write_text(json.dumps(repos, indent=1) + "\n")
    (DATA / "fetched_at.json").write_text(json.dumps({"date": datetime.now(timezone.utc).strftime("%Y-%m-%d")}) + "\n")
    print(f"{len(repos)} public repositories, {sum(len(r['labels']) for r in repos)} labels")


if __name__ == "__main__":
    main()
