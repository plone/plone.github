"""Reduce the audit data to the figures the proposal quotes.

Pure helpers (``is_dead``, ``dead_labels``) and ``compute(data_dir)``, whose
keys are the only placeholders the proposal text may use. CLI writes
data/numbers.json.
"""
import csv
import json
import re
from pathlib import Path

from scripts.common import DATA, normalize

EXEMPT = {"11 prio: blocker"}          # rare by nature; low usage is what the word means
DEAD_MAX_RECENT = 10                   # items created since 2025-01-01
DEAD_MAX_OPEN = 20                     # open issues + open PRs
REDUNDANT = [                          # used, but a native GitHub feature covers them
    "01 type: bug", "03 type: feature (plip)", "04 type: enhancement", "05 type: question",
    "22 status: in-progress", "24 status: ready", "32 needs: review",
]
LABEL_FILTER_RE = re.compile(r'label:"?\d\d')


def is_dead(created_since: int, open_items: int, name: str) -> bool:
    return created_since <= DEAD_MAX_RECENT and open_items <= DEAD_MAX_OPEN and name not in EXEMPT


def dead_labels(rows: list[dict]) -> list[str]:
    return [r["label"] for r in rows
            if is_dead(int(r["created_since_2025_any_state"]),
                       int(r["open_issues"]) + int(r["open_prs"]), r["label"])]


def fetch_date(data_dir: Path) -> str:
    """The day the data was fetched, recorded by fetch_labels (never a file mtime)."""
    return json.load((data_dir / "fetched_at.json").open())["date"]


def _usage(data_dir: Path) -> list[dict]:
    with (data_dir / "canonical_label_usage.csv").open(newline="") as f:
        return list(csv.DictReader(f))


def _open_issues(rows: list[dict], label: str) -> int:
    return next(int(r["open_issues"]) for r in rows if r["label"] == label)


def _repos_with(repos: list[dict], label: str) -> int:
    want = normalize(label)
    return sum(1 for r in repos if any(normalize(l["name"]) == want for l in r["labels"]))


def compute(data_dir: Path = DATA) -> dict:
    repos = json.load((data_dir / "plone_labels.json").open())
    conf = json.load((data_dir / "conformance.json").open())
    feats = json.load((data_dir / "features_in_use.json").open())
    boards = json.load((data_dir / "projects.json").open())["boards"]
    usage = _usage(data_dir)
    active = [r for r in repos if not r["archived"]]
    aconf = [c for c in conf if not c["archived"]]
    cls = lambda name: sum(1 for c in aconf if c["cls"] == name)  # noqa: E731
    dead = dead_labels(usage)
    return {
        "date": fetch_date(data_dir),
        "repos_total": len(repos),
        "repos_active": len(active),
        "repos_archived": len(repos) - len(active),
        "repos_full": cls("A full") + cls("B full+extras"),
        "repos_full_plain": cls("A full"),
        "repos_full_extras": cls("B full+extras"),
        "repos_near": cls("C near"),
        "repos_partial": cls("D partial") + cls("E traces"),
        "repos_none": cls("F none"),
        "drift_24_repos": sum(1 for c in aconf if "24 status: deferred" in c["drift"]),
        "dead_count": len(dead),
        "dead_labels": dead,
        "redundant_count": len(REDUNDANT),
        "redundant_labels": REDUNDANT,
        "a11y_label_repos": _repos_with(active, "99 tag: UX Accessibility"),
        "gfi_hidden_open": _open_issues(usage, "41 lvl: easy"),
        "hw_hidden_open": _open_issues(usage, "31 needs: help"),
        "needs_triage_repos": _repos_with(active, "30 needs: triage"),
        "typed_open_issues": feats["typed_open_issues"],
        "typed_share_since_2025_06": round(100 * feats["typed_since_2025_06"] / max(1, feats["issues_since_2025_06"])),
        "projects_total": len(boards),
        "projects_open": sum(1 for b in boards if not b["closed"]),
        "open_draft_prs": feats["open_draft_prs"],
        "open_automerge_prs": feats["open_automerge_prs"],
        "open_regressions": feats["open_regressions"],
        "core_repos_without_discussions": sum(1 for v in feats["discussions_enabled"].values() if not v),
        "label_filtered_views": sum(1 for b in boards if not b["closed"]
                                    for v in b["views"]["nodes"] if LABEL_FILTER_RE.search(v["filter"] or "")),
        "issue_fields_members_only": sum(1 for f in feats["issue_fields"] if f["visibility"] == "organization_members_only"),
        "blank_issues_enabled": feats["blank_issues_enabled"],
    }


def main() -> None:
    numbers = compute()
    (DATA / "numbers.json").write_text(json.dumps(numbers, indent=1) + "\n")
    print(json.dumps(numbers, indent=1))


if __name__ == "__main__":
    main()
