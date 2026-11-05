"""Usage of the 27 canonical labels across public, non-archived repositories.

Writes data/canonical_label_usage.csv with columns
label,open_issues,open_prs,created_since_2025_any_state.
"""
import csv

from scripts.common import DATA, SINCE, canonical_labels, gh_escape
from scripts.gh_graphql import gql


def counts(labels: list[str], suffix: str) -> list[int]:
    parts = []
    for i, label in enumerate(labels):
        q = gh_escape(f'org:plone is:public archived:false label:"{label}" {suffix}')
        parts.append(f's{i}: search(type: ISSUE, query: "{q}") {{ issueCount }}')
    data = gql("{ " + " ".join(parts) + " }")
    return [data[f"s{i}"]["issueCount"] for i in range(len(labels))]


def main() -> None:
    labels = canonical_labels()
    open_issues = counts(labels, "is:issue is:open")
    open_prs = counts(labels, "is:pr is:open")
    recent = counts(labels, f"created:>={SINCE}")
    with (DATA / "canonical_label_usage.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["label", "open_issues", "open_prs", "created_since_2025_any_state"])
        for row in zip(labels, open_issues, open_prs, recent):
            w.writerow(row)
    print(f"{len(labels)} labels written")


if __name__ == "__main__":
    main()
