"""How closely each public repository follows the 2015 label scheme.

Pure functions (``canon_from_sheet``, ``normalize``, ``classify``) plus a CLI
that writes data/plone_label_conformance.csv and data/conformance.json.
"""
import csv
import json
import re
from pathlib import Path

from scripts.common import BOT_LABELS, DATA, DEFINITIONS, SHEET_CSV, load_repos, normalize  # noqa: F401

CLASSES = (
    (27, "A full"),
    (22, "C near"),
    (8, "D partial"),
    (1, "E traces"),
)


def canon_from_sheet(csv_path: Path) -> dict[str, str]:
    """Label -> description from the sheet's two-column layout, normalized,
    without the proposed ``06`` row and the free-form ``99`` namespace."""
    canon: dict[str, str] = {}
    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    for row in rows[1:]:
        for label_col, desc_col in ((1, 2), (5, 6)):
            if len(row) <= label_col:
                continue
            label = row[label_col].strip()
            if not label or not label[:2].isdigit() or label.startswith(("06", "99")):
                continue
            desc = row[desc_col].strip() if len(row) > desc_col else ""
            canon[normalize(label)] = desc
    return canon


def body(name: str) -> str:
    """Strip the numeric prefix: '25 status: deferred' -> 'status: deferred'."""
    return re.sub(r"^\d\d:?\s*", "", normalize(name))


def classify(labels: list[str], canon: set[str]) -> dict:
    """Score a repository's label names against the canonical set."""
    canon_norm = {normalize(c) for c in canon}
    by_body = {body(c): c for c in canon_norm}
    present = {normalize(l) for l in labels}
    exact = canon_norm & present
    drift = {}
    for n in present:
        b = body(n)
        if n not in canon_norm and b in by_body and by_body[b] not in present:
            drift[n] = by_body[b]
    missing = canon_norm - exact - set(drift.values())
    tag99 = [l for l in labels if normalize(l).startswith("99 tag:")]
    bad99 = [l for l in labels if normalize(l).startswith("99") and not normalize(l).startswith("99 tag:")]
    extras = [l for l in labels
              if normalize(l) not in canon_norm and normalize(l) not in drift
              and not normalize(l).startswith("99") and l not in BOT_LABELS]
    score = len(exact) + len(drift)
    if score == 27:
        cls = "A full" if not extras and not bad99 else "B full+extras"
    else:
        cls = "F none"
        for threshold, name in CLASSES[1:]:
            if score >= threshold:
                cls = name
                break
    return {"score": score, "cls": cls, "missing": sorted(missing), "drift": drift,
            "extras": extras, "tag99": tag99, "bad99": bad99}


def main() -> None:
    canon = set(canon_from_sheet(SHEET_CSV))
    listed_2019 = set(json.load(DEFINITIONS.open())["ORGANIZATIONS"]["plone"])
    rows = []
    for repo in load_repos():
        r = classify([l["name"] for l in repo["labels"]], canon)
        rows.append({"repo": repo["name"], "archived": repo["archived"], "created": repo["createdAt"][:10],
                     "in_2019_definitions": repo["name"] in listed_2019, **r})
    rows.sort(key=lambda x: (x["archived"], x["cls"], x["repo"].lower()))
    (DATA / "conformance.json").write_text(json.dumps(rows, indent=1) + "\n")
    with (DATA / "plone_label_conformance.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["repo", "archived", "created", "class", "canonical_present", "in_2019_definitions",
                    "missing", "number_drift", "non_scheme_extras", "99_tags"])
        for x in rows:
            w.writerow([x["repo"], x["archived"], x["created"], x["cls"], x["score"], x["in_2019_definitions"],
                        "; ".join(x["missing"]), "; ".join(f"{k} -> {v}" for k, v in x["drift"].items()),
                        "; ".join(x["extras"] + x["bad99"]), "; ".join(x["tag99"])])
    print(f"{len(rows)} repositories classified")


if __name__ == "__main__":
    main()
