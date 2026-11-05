from scripts.gh_graphql import is_public


def test_is_public():
    assert is_public({"isPrivate": False})
    assert not is_public({"isPrivate": True})
    assert not is_public({})


def _repo(name, private):
    return {
        "name": name, "isPrivate": private, "isArchived": False, "isFork": False,
        "createdAt": "2020-01-01T00:00:00Z",
        "labels": {"nodes": [{"name": "bug", "description": "", "color": "ff0000"}],
                   "pageInfo": {"hasNextPage": False, "endCursor": None}},
    }


def test_fetch_filters_private(monkeypatch):
    from scripts import fetch_labels
    pages = [{"nodes": [_repo("pub", False), _repo("sec", True)],
              "pageInfo": {"hasNextPage": False, "endCursor": None}}]
    monkeypatch.setattr(fetch_labels, "fetch_pages", lambda: iter(pages))
    repos = fetch_labels.collect()
    assert [r["name"] for r in repos] == ["pub"]
    assert repos[0]["visibility"] == "public"
    assert repos[0]["labels"] == [{"name": "bug", "description": "", "color": "ff0000"}]


def test_data_files_public_only():
    import json
    from pathlib import Path
    repos = json.load((Path(__file__).resolve().parents[1] / "data/plone_labels.json").open())
    assert repos, "data/plone_labels.json is empty"
    assert all(r["visibility"] == "public" for r in repos)
    assert len(repos) < 457  # the all-repositories count of the 2026-11-05 audit
