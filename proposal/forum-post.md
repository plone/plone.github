<!-- Discourse title: Proposal: fewer labels, a lighter process for Plone's issue trackers -->
<!-- Paste everything below this line into the post body; Discourse drops these comments. -->

2015, or eleven years ago, I proposed a labeling system for Plone. I wrote a script that put 27 (!) numbered labels on every Plone Orga repository. GitHub got a whole bunch of new features since then: issue types and fields, Discussions, boards, draft PRs, close reasons, sub-issues.

Our scheme is the same, last applied 2019. An audit of the organization with its repos shows that this system partly (or should I say largely?) failed: unused labels or meanwhile duplicates of a GitHub feature.

The short version of what I propose:

- **8 plain labels** instead of 27: `needs: triage`, `needs: info`, `help wanted`, `good first issue`, `blocker`, `accessibility`, `i18n`, `documentation`.
- **GitHub features for the rest**: issue types, the Priority and Effort fields, Discussions, milestones, close reasons, boards.
- **Issues are for work with a definition of done.** Questions and ideas get a home in Discussions or here on the forum, where they can find their Plonistas.
- **Forms set the first state**, so a maintainer removes a label instead of remembering a convention. `good first issue` and `help wanted` work with GitHub's newcomer discovery again.
- **An invitation, not a rule.** Nothing obliges anyone, an unlabeled issue stays a fine issue, and every team keeps its own local labels and automation. The one central step costs a repository nothing.

The full proposal, with the reasoning, the data and the complete mapping from old to new, is a PDF: [proposal.pdf, release proposal-v1](https://github.com/plone/plone.github/releases/download/proposal-v1/proposal.pdf). Sources and audit scripts: [plone/plone.github](https://github.com/plone/plone.github).

**What I am asking you!** Read it and tell me what would not work for the repository you work with or your team. Here or on Discord. In about 4 weeks I plan to open a PLIP-style issue in plone/plone.github, look for a seconder and +1s from team leads, release managers, Plonistas with an opinion. And if nobody objects, roll it out scripted. The documentation team is going to be in the loop, since the contributing docs change with it a bit.

---

*AI-transparency: the whole analysis, process and PDF generation was assisted-by Claude Fable 5.1*
