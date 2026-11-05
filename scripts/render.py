"""Assemble proposal/src/*.md, fill {{placeholders}} from data/numbers.json,
write build/proposal.md."""
import json
import re
from pathlib import Path

from scripts.common import DATA, DEFINITIONS, ROOT, SHEET_CSV
from scripts.conformance import canon_from_sheet
from scripts.numbers import LABEL_FILTER_RE, REDUNDANT, dead_labels

SRC = ROOT / "proposal/src"
BUILD = ROOT / "build"
PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")


def render(text: str, values: dict) -> str:
    def sub(m):
        key = m.group(1)
        if key not in values:
            raise KeyError(key)
        v = values[key]
        return ", ".join(map(str, v)) if isinstance(v, list) else str(v)
    out = PLACEHOLDER.sub(sub, text)
    if "{{" in out:
        raise ValueError("leftover placeholder: " + out[out.index("{{"):][:40])
    return out


def assemble(src_dir: Path) -> str:
    parts = [p.read_text(encoding="utf-8").strip("\n") for p in sorted(src_dir.glob("*.md"))]
    return "\n\n".join(parts) + "\n"


def _table(header: list[str], rows: list[list], widths: str = "") -> str:
    sep = widths or "|".join("---" for _ in header)
    out = ["| " + " | ".join(header) + " |", "|" + sep + "|"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def appendix_b(data_dir: Path) -> str:
    """The audit in numbers, generated from data/."""
    import csv
    with (data_dir / "canonical_label_usage.csv").open(newline="") as f:
        usage = list(csv.DictReader(f))
    dead = set(dead_labels(usage))
    conf = [c for c in json.load((data_dir / "conformance.json").open()) if not c["archived"]]
    feats = json.load((data_dir / "features_in_use.json").open())
    boards = json.load((data_dir / "projects.json").open())
    samples = json.load((data_dir / "projects_items_sample.json").open())

    def verdict(label):
        return "dead" if label in dead else "redundant" if label in REDUNDANT else "in use"

    parts = ["# The audit in numbers", "",
             "All figures cover the public repositories of the organization and are produced by the "
             "scripts in `scripts/`. Dead: at most ten items created since 2025-01-01 and at most "
             "twenty open; `11 prio: blocker` is exempt as rare by nature. Redundant: in use, but a native "
             "feature covers it.", "",
             "## Usage of the 2015 labels", "",
             _table(["Label", "Open issues", "Open PRs", "Created since 2025", "Verdict"],
                    [[f"`{u['label']}`", u["open_issues"], u["open_prs"], u["created_since_2025_any_state"],
                      verdict(u["label"])] for u in usage]), "",
             "## How closely active repositories follow the scheme", ""]
    classes = {}
    for c in conf:
        classes[c["cls"]] = classes.get(c["cls"], 0) + 1
    parts += [_table(["Class", "Repositories"], [[k, v] for k, v in sorted(classes.items())]), "",
              f"Repositories whose scheme says `24 status: deferred` instead of `25`: "
              f"{sum(1 for c in conf if '24 status: deferred' in c['drift'])}.", "",
              "## Project boards", "",
              f"{len(boards['boards'])} public boards; private boards are not listed. "
              f"Views that filter on a 2015 label:", ""]
    views = [[b["title"], v["name"], f"`{v['filter']}`"] for b in boards["boards"] if not b["closed"]
             for v in b["views"]["nodes"] if LABEL_FILTER_RE.search(v["filter"] or "")]
    parts += [_table(["Board", "View", "Filter"], views) if views else "None.", "",
              "Labels carried by the items of the key public boards (sample of the first hundred items "
              "from public repositories):", ""]
    parts += [_table(["Board", "Items", "Sampled", "Open (of sample)", "Most frequent labels (of sample)"],
                     [[s["title"], s["total"], s["from_public_repos"], s["open"],
                       ", ".join(f"`{l}` ({n})" for l, n in s["labels"][:3])] for s in samples.values()]), "",
              "## Native features in use", "",
              _table(["Feature", "State"], [
                  ["Issue types configured", ", ".join(feats["issue_types"])],
                  ["Open issues with a type", feats["typed_open_issues"]],
                  ["Issues created since 2025-06 with a type",
                   f"{feats['typed_since_2025_06']} of {feats['issues_since_2025_06']}"],
                  ["Issue fields", "; ".join(f"{f['name']} ({f['visibility'].replace('_', ' ')})" for f in feats["issue_fields"])],
                  ["Discussions enabled", ", ".join(f"{k}: {'yes' if v else 'no'}" for k, v in feats["discussions_enabled"].items())],
                  ["Open draft pull requests", feats["open_draft_prs"]],
                  ["Open pull requests with auto-merge", feats["open_automerge_prs"]],
                  ["Open issues labelled regression", feats["open_regressions"]],
                  ["`blank_issues_enabled` in the org templates", feats["blank_issues_enabled"]],
              ])]
    return "\n".join(parts) + "\n"


def appendix_c(sheet_csv: Path, definitions_json: Path) -> str:
    """The 2015 scheme for reference: label, colour, the sheet's description."""
    canon = canon_from_sheet(sheet_csv)
    defs = json.load(definitions_json.open())
    colours = {k.lower(): v for k, v in defs["LABELS"].items()}
    rows = [[f"`{label}`", f"`{colours.get(label, '')}`", desc] for label, desc in sorted(canon.items())]
    return "\n".join([
        "# The 2015 scheme for reference", "",
        f"Twenty-seven labels, defined in the archived sheet and in `definitions.json` of the 2019 tool, "
        f"which listed {len(defs['ORGANIZATIONS']['plone'])} repositories. Free-form `99 tag:` labels "
        f"and the `06 type: accessibility` row proposed in 2026 are not part of the set.", "",
        _table(["Label", "Colour", "Description in the sheet"], rows),
    ]) + "\n"


def version() -> str:
    """git describe of the checkout: the tag on a release build, else a short hash."""
    import subprocess
    try:
        return subprocess.run(["git", "describe", "--tags", "--always", "--dirty"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip() or "unreleased"
    except (OSError, subprocess.CalledProcessError):
        return "unreleased"


def main() -> None:
    numbers = {**json.load((DATA / "numbers.json").open()), "version": version()}
    BUILD.mkdir(exist_ok=True)
    parts = []
    for p in sorted(SRC.glob("*.md")):
        if p.name.startswith("99-"):
            parts += [appendix_b(DATA), appendix_c(SHEET_CSV, DEFINITIONS)]
        parts.append(p.read_text(encoding="utf-8").strip("\n"))
    (BUILD / "proposal.md").write_text(render("\n\n".join(parts) + "\n", numbers), encoding="utf-8")
    print(f"build/proposal.md written from {len(list(SRC.glob('*.md')))} source files plus appendices B and C")


if __name__ == "__main__":
    main()
