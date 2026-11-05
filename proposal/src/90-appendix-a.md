```{=latex}
\appendix
```

# Complete mapping, 2015 to 2026

*Rename*: the same label under a new name; existing issues keep it. *Move*: the script sets the issue type or the issue field and removes the label; the fact moves to a native field. *Retire*: deleted where no item carries it, archived where one still does, so history stays and a team can bring it back. *Repo-local*: outside the shared set; the rollout never touches it, the row is a recommendation.

| 2015 label | 2026 | Class |
|---------------|----------------------|------|
| `01 type: bug` | Issue type `Bug` | Move |
| `02 type: regression` | Issue type `Bug`, or `Regression` if the organization adds that type | Move |
| `03 type: feature (plip)` | Issue type `PLIP` | Move |
| `04 type: enhancement` | Issue type `Feature` | Move |
| `05 type: question` | A Discussion; converting the existing ones is each team's call | Retire |
| `06 type: plip task` (Volto, Aurora) | Issue type `Task` as a sub-issue of the PLIP | Move |
| `11 prio: blocker` | `blocker` | Rename |
| `12 prio: high` | Issue field Priority = High | Move |
| `13 prio: normal` | Nothing; normal is the default | Retire |
| `14 prio: low` | Issue field Priority = Low | Move |
| `21 status: confirmed` | The absence of `needs: triage` | Retire |
| `22 status: in-progress` | Assignee, draft pull request, board Status | Retire |
| `23 status: testing` | Status checks | Retire |
| `24 status: ready` | Auto-merge, or the merge click | Retire |
| `24`/`25 status: deferred` | Milestone, board, or a Discussion | Retire |
| `26 status: blocked` (Volto) | Issue dependencies | Repo-local |
| `27 status: stale` (Volto) | The team's stale automation | Repo-local |
| `30 needs: triage` (Volto, Aurora) | `needs: triage` | Rename |
| `30.1 needs: confirmation` (Volto) | `needs: info` | Rename |
| `31 needs: help` | `help wanted` | Rename |
| `32 needs: review` | Review requests, CODEOWNERS | Retire |
| `33 needs: docs` | `documentation` | Rename |
| `34 needs: tests` | Review and checks | Retire |
| `35 needs: rebase` | Conflict indicator, *Update branch* | Retire |
| `36 needs: cla` | The Contributors Agreement check | Retire |
| `37 needs: release` | The release status check | Retire |
| `41 lvl: easy` | `good first issue` | Rename |
| `42 lvl: moderate` | Issue field Effort, optional | Retire |
| `43 lvl: complex` | Issue field Effort, optional | Retire |
| `51 target: patch` | Milestone of the patch release; towncrier `bugfix` | Retire |
| `52 target: minor` | Milestone of the minor release; towncrier `feature` | Retire |
| `53 target: major` | Milestone of the major release; towncrier `breaking` | Retire |
| `99 tag: UX Accessibility` | `accessibility` | Rename |
| `99 tag: documentation` | `documentation` | Rename |
| `99 tag: duplicate`, `invalid`, `wontfix` | Close reasons | Repo-local |
| `99 tag: Plone 4.3.x`, `5.x`, `6.x` and friends | Milestones | Repo-local |
| `99 tag: sprint` | The sprint's board | Repo-local |
| every other `99 tag:` label | The team decides; the prefix may go | Repo-local |

Labels on pull requests that move to an issue type or an issue field are removed from the pull request, because neither exists there: the towncrier fragment carries the type, and priority belongs to the issue.
