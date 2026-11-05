# Why now

The scheme was designed for a GitHub that no longer exists. The first commit of the `plone.github` tool dates from 2015, its last run from October 2019. Everything in the right column below arrived after the scheme was drawn up, most of it after the tool was last run.

| Year | GitHub feature | What it replaces in the scheme |
|---|---|---|
| 2019 | Draft pull requests | `status: in-progress` on PRs |
| 2020 | Discussions | `type: question`, parked ideas |
| 2021 | Auto-merge | `status: ready` |
| 2022 | Close reasons; Projects with custom fields | `tag: duplicate`, `tag: wontfix`; `status:` and `prio:` for planning |
| 2023 | Merge queue | `status: testing`, `status: ready` at scale |
| 2025 | Issue types; sub-issues; dependencies | `type:` labels; `plip task`; `status: blocked` |
| 2026 | Issue fields; label archiving | `prio:` and `lvl:` labels; retiring labels without losing history |

## What the audit found

All figures are from {{date}}, cover the {{repos_total}} public repositories of the organization ({{repos_active}} active, {{repos_archived}} archived), and can be reproduced from the data and scripts in the repository.

- **The scheme is everywhere; a third of it is unused and another quarter duplicates a feature.** {{repos_full}} of the active repositories carry all twenty-seven labels; {{repos_none}} carry none, almost all of them infrastructure, team and retired-project repositories. A label counts as *dead* here when at most ten items were created with it since January 2025 and at most twenty items carrying it are open. That is true for {{dead_count}} labels: {{dead_labels}}. Another {{redundant_count}} are in use but duplicate a native feature: {{redundant_labels}}.
- **Two sources of truth drifted apart.** The 2019 tool says `25 status: deferred`; the organization's "default labels for new repositories" setting says `24 status: deferred`, which collides with `24 status: ready`. Most repositories created since late 2019 have the collision, {{drift_24_repos}} of them today.
- **Newcomers cannot find us.** GitHub's contributor discovery keys on the exact label names `good first issue` and `help wanted`. The 2019 migration renamed both away. Today {{gfi_hidden_open}} open issues are marked `41 lvl: easy` and {{hw_hidden_open}} are marked `31 needs: help`, and GitHub shows none of them to a newcomer.
- **The organization's own defaults are broken by the scheme they feed.** The issue templates in `plone/.github`, which every repository without its own templates inherits, set `30 needs: triage` on each bug report. GitHub silently drops a template label that does not exist in the repository, and that label exists in {{needs_triage_repos}} repositories.
- **The native features are already here, without a plan.** Issue types are configured and carry {{typed_open_issues}} open issues, about {{typed_share_since_2025_06}} percent of the issues created since mid-2025. Issue fields have been switched on since May 2026 with GitHub's four defaults, {{issue_fields_members_only}} of them visible to members only, and almost nobody sets them. Of the six core repositories we checked, {{core_repos_without_discussions}} have Discussions switched off. {{open_draft_prs}} pull requests are open as drafts; {{open_automerge_prs}} have auto-merge enabled.
- **Ideas have no home.** In the large trackers many open issues are ideas and questions without an owner. They are neither bugs nor planned work, and the tracker gives them no place to grow: they sit between open and closed, and neither state does them justice.
