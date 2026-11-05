# Proposal: fewer labels, a lighter process for Plone's issue trackers

Eleven years ago I wrote the tool that put twenty-seven numbered labels on every Plone repository. GitHub has grown a lot since then: issue types and fields, Discussions, boards, draft PRs, close reasons, sub-issues. Our scheme has not, and an audit of the organization shows that about half of it is unused or duplicates a GitHub feature.

The short version of what I propose:

- **Eight plain labels** instead of twenty-seven: `needs: triage`, `needs: info`, `help wanted`, `good first issue`, `blocker`, `accessibility`, `i18n`, `documentation`.
- **GitHub features for the rest**: issue types, the Priority and Effort fields, Discussions, milestones, close reasons, boards.
- **Issues are for work with a definition of done.** Questions and ideas get a home in Discussions or here on the forum, where they can find their people.
- **Forms set the first state**, so a maintainer removes a label instead of remembering a convention. `good first issue` and `help wanted` work with GitHub's newcomer discovery again.
- **An invitation, not a rule.** Nothing obliges anyone, an unlabeled issue stays a fine issue, and every team keeps its own local labels and automation. The one central step costs a repository nothing.

The full proposal, with the reasoning, the data and the complete mapping from old to new, is a PDF: <PDF-URL>. Sources and audit scripts: https://github.com/plone/plone.github.

**What I am asking for.** Read it and tell me what would not work for your repository or team, here or on Discord. In about four weeks I will open a PLIP-style issue in plone/plone.github, look for a seconder and +1s from team leads and release managers, and if nobody objects, roll it out scripted. The documentation team is in the loop, since the contributing docs change with it.

Assisted-by: Claude Fable 5.1
