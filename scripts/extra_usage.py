"""Usage of every label outside the 2015 scheme on active public repositories.

Writes data/extra_label_usage.json (per repo and label) and the aggregate
data/non_scheme_labels.csv.
"""
import csv
import json
from collections import defaultdict

from scripts.common import DATA, SINCE, canonical_labels, gh_escape, load_repos, normalize
from scripts.gh_graphql import gql


def non_scheme_pairs(repos: list[dict]) -> list[tuple[str, str]]:
    canon = {normalize(l) for l in canonical_labels()}
    pairs = []
    for repo in repos:
        for label in repo["labels"]:
            n = normalize(label["name"])
            if n not in canon and n != "24 status: deferred":
                pairs.append((repo["name"], label["name"]))
    return pairs


def label_counts(pairs: list[tuple[str, str]], batch: int = 60) -> dict:
    result = {}
    for start in range(0, len(pairs), batch):
        chunk = pairs[start:start + batch]
        by_repo = defaultdict(list)
        for j, (repo, label) in enumerate(chunk):
            by_repo[repo].append((j, label))
        parts = []
        for k, (repo, labels) in enumerate(by_repo.items()):
            inner = " ".join(
                f'l{j}: label(name: {json.dumps(label)}) {{ openI: issues(states: OPEN) {{ totalCount }} '
                f'allI: issues {{ totalCount }} openP: pullRequests(states: OPEN) {{ totalCount }} '
                f'allP: pullRequests {{ totalCount }} }}'
                for j, label in labels)
            parts.append(f'r{k}: repository(owner: "plone", name: {json.dumps(repo)}) {{ {inner} }}')
        data = gql("{ " + " ".join(parts) + " }")
        for k, (repo, labels) in enumerate(by_repo.items()):
            for j, label in labels:
                node = data[f"r{k}"][f"l{j}"]
                if node:
                    result[(repo, label)] = {key: node[key]["totalCount"] for key in ("openI", "allI", "openP", "allP")}
    return result


def recent_counts(keys: list[tuple[str, str]], batch: int = 40) -> dict:
    result = {}
    for start in range(0, len(keys), batch):
        chunk = keys[start:start + batch]
        parts = []
        for j, (repo, label) in enumerate(chunk):
            q = gh_escape(f'repo:plone/{repo} label:"{label}" created:>={SINCE}')
            parts.append(f's{j}: search(type: ISSUE, query: "{q}") {{ issueCount }}')
        data = gql("{ " + " ".join(parts) + " }")
        for j, key in enumerate(chunk):
            result[key] = data[f"s{j}"]["issueCount"]
    return result


def aggregate(rows: list[dict]) -> list[dict]:
    agg = defaultdict(lambda: {"repos": [], "openI": 0, "openP": 0, "allI": 0, "allP": 0, "recent": 0})
    for r in rows:
        a = agg[r["label"]]
        a["repos"].append(r["repo"])
        for key in ("openI", "openP", "allI", "allP", "recent"):
            a[key] += r[key]
    out = [{"label": label, **a} for label, a in agg.items()]
    out.sort(key=lambda a: (-a["recent"], -(a["openI"] + a["openP"]), a["label"]))
    return out


def main() -> None:
    pairs = non_scheme_pairs(load_repos(active_only=True))
    counts = label_counts(pairs)
    used = [k for k in pairs if k in counts and counts[k]["allI"] + counts[k]["allP"] > 0]
    recent = recent_counts(used)
    rows = [{"repo": repo, "label": label, **v, "recent": recent.get((repo, label), 0)}
            for (repo, label), v in counts.items()]
    (DATA / "extra_label_usage.json").write_text(json.dumps(rows, indent=1) + "\n")
    with (DATA / "non_scheme_labels.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["label", "repo_count", "created_since_2025", "open_issues", "open_prs", "all_issues", "all_prs", "repos"])
        for a in aggregate(rows):
            w.writerow([a["label"], len(a["repos"]), a["recent"], a["openI"], a["openP"], a["allI"], a["allP"],
                        "; ".join(sorted(a["repos"]))])
    print(f"{len(rows)} repo/label pairs, {len(aggregate(rows))} distinct labels")


if __name__ == "__main__":
    main()
