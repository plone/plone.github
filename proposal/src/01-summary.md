# Management summary

Plone's repositories on GitHub still carry the label scheme we introduced in 2015: twenty-seven numbered labels, rolled out by a script and documented in a Google Sheet. GitHub has changed since then. It now has issue types and fields, Discussions, boards, draft pull requests, checks, close reasons, sub-issues and dependencies. Most of what the labels once encoded has a native home, and the audit behind this proposal shows that the community has quietly stopped using {{dead_count}} of the labels, while {{redundant_count}} more duplicate a GitHub feature.

What people experience today: a reporter opens an issue and often hears nothing, because nobody can tell which issues nobody has looked at yet. A newcomer finds little to start with, because the {{gfi_hidden_open}} issues we marked as easy and the {{hw_hidden_open}} we marked as wanting help carry names GitHub's newcomer discovery does not recognise. An idea that is not yet a plan sits open for years, because an issue tracker has no good place for ideas. And a maintainer has to learn a numbering convention first.

**The proposal in five points**

1. **Eight plain labels**, kept only where GitHub has no feature for the fact: `needs: triage`, `needs: info`, `help wanted`, `good first issue`, `blocker`, `accessibility`, `i18n`, `documentation`.
2. **GitHub features take over the rest**: issue types for bug, feature, task and PLIP; the Priority and Effort fields; Discussions for questions and ideas; draft pull requests and checks for the state of a PR; milestones for release targets; close reasons; boards for planning.
3. **Issue forms set the first state.** A new issue arrives typed and marked `needs: triage`. The common move for a maintainer is to remove a label or click a native control, never to remember a convention.
4. **Issues are for work with a definition of done.** Questions and ideas get a home in Discussions or on community.plone.org, where they can find their people. Moving an idea there is hospitality, not rejection.
5. **One source of truth and an automatic check**, so that the drift since the tool was last run in 2019 cannot repeat and a new repository arrives with everything in place.

**What changes for whom**

| | |
|---|---|
| A small package | Nothing to do. The labels arrive by themselves. |
| A large repository | Keeps its local labels and automation; gains a first-response view, a place for ideas, boards that carry the status. |
| A contributor | `good first issue` and `help wanted` work with GitHub's discovery again; every new issue gets a first response. |
| A release manager | `blocker` as the one alarm everybody sees, graded priority in a field, milestones, towncrier as before. |

This is an invitation, not a rule. An issue without labels or type stays a perfectly fine issue, as it always was in Plone. The only part that is not optional is what the organization admin does once, centrally, and that asks nothing of anyone.

**Next steps.** Feedback on the forum and on Discord for about four weeks; then a PLIP-style issue in `plone/plone.github` with a seconder, +1s, and a scripted rollout (section 9).

```{=latex}
\newpage
\tableofcontents
\newpage
```
