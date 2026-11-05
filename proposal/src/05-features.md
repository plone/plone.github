# Where GitHub features take over

Every label that disappears from the shared set has a native home. The table groups the old scheme; the complete mapping, label by label and with its migration class, is Appendix A.

![From twenty-seven labels to GitHub features and eight labels](build/diagrams/then-now.pdf){width=100%}

| 2015 scheme | 2026 |
|-----------|-----------------|
| `01 type: bug`, `04 type: enhancement`, `03 type: feature (plip)` | **Issue types** `Bug`, `Feature`, `PLIP`, already configured for the organization and set by the issue forms. `Regression` may be added as a fifth type; otherwise a regression is a `Bug`. |
| `05 type: question` | A **Discussion** in the repository, or a thread on community.plone.org (section 6). |
| `06 type: plip task` (Volto, Aurora) | Issue type `Task` as a **sub-issue** of the PLIP. Sub-issues work across repositories; CMFPlone PLIPs already have children in volto and documentation. |
| `11 prio: blocker` | `blocker`, renamed. |
| `12 prio: high`, `13 prio: normal`, `14 prio: low` | The **Priority issue field**. High and low are migrated into it; normal is the default and needs no migration. On pull requests the label is simply removed; priority belongs to the issue. |
| `21 status: confirmed` | The absence of `needs: triage`. |
| `22 status: in-progress` | The assignee, a **draft pull request**, and the Status field of a board. |
| `23 status: testing`, `24 status: ready` | **Status checks**; *Enable auto-merge* where the branch has required checks; otherwise the maintainer's merge click. |
| `25 status: deferred` | A milestone or a board; a parked idea becomes a Discussion. |
| `26 status: blocked` (Volto) | **Issue dependencies**: *blocked by* and *blocking*, with the filters `is:blocked` and `is:blocking`. |
| `30 needs: triage`, `30.1 needs: confirmation` (Volto) | `needs: triage`, `needs: info`. |
| `31 needs: help` | `help wanted`. |
| `32 needs: review` | **Review requests** and CODEOWNERS. |
| `33 needs: docs` | `documentation`, renamed. It was used as the documentation team's cross-repository feed, not as a state. |
| `34 needs: tests` | Review and checks. |
| `35 needs: rebase` | GitHub's conflict indicator and *Update branch*. |
| `36 needs: cla` | The *Plone Contributors Agreement verifier* check that already runs on every pull request. |
| `37 needs: release` | The *release status* check of the shared workflows and the release tooling. |
| `41 lvl: easy` | `good first issue`. |
| `42 lvl: moderate`, `43 lvl: complex` | The **Effort issue field**, for teams that want it. |
| `51 target: patch`, `52 target: minor`, `53 target: major` | **Milestones** per release line, and the towncrier fragment type that the changelog check already enforces on every pull request. |
| `99 tag: UX Accessibility` | `accessibility`. |
| `99 tag: duplicate`, `99 tag: invalid`, `99 tag: wontfix` | **Close reasons**: *duplicate*, *not planned*. |
| `99 tag: Plone 5.x`, `99 tag: Plone 6.x` and friends | Milestones. |
| `99 tag: sprint` | Project boards; the organization has one per sprint already. |
| every other `99 tag:` label | Repo-local. The team decides, and may drop the prefix. |

## Three features worth a closer look

**Issue fields.** Organization issue fields reached general availability in July 2026: typed metadata defined once for the organization, shown in the issue list, filterable with `field.priority:high`. GitHub's own words for them are a way "to avoid relying on labels". The Plone organization has had them switched on since May 2026 with the four defaults, Priority, Effort, Start date and Target date, all visible to members only, and almost nobody sets them. The proposal makes Priority and Effort public and gives them a job. Two limits to know: fields exist on issues, not on pull requests, and an issue form cannot preset them. Both fit the rule that priority is a triage decision made on the issue.

**Project boards.** Of the organization's {{projects_total}} boards, {{projects_open}} are open. Every one of them groups by its Status field, which is why the `status:` labels can go. Exactly {{label_filtered_views}} views on the public boards filter on an old label, both of them easy to point at an issue type instead. Three labels feed boards today and keep working as filters after the rename: `99 tag: UX Accessibility` feeds the Accessibility board, `03 type: feature (plip)` feeds the PLIPs board where most items already carry the PLIP type, and `33 needs: docs` feeds the Plone Documentation board. Their auto-add workflows are the one thing to check by hand on rollout day.

**Label archiving.** Since August 2026 a label can be archived instead of deleted: it stays on every existing issue with its history, disappears from the picker so it cannot spread, and comes back with one click. This is how retired labels still in use are handled. Nothing is ever removed from an issue.
