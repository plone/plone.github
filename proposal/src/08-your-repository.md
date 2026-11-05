# What this means for your repository

**Done centrally, zero effort for you.** The eight shared labels exist; the old labels are renamed, moved into a native field, or archived, as Appendix A lists for each of them. Nothing else changes. This is the only part that is not optional, and it asks nothing of anyone.

**Invitations, each a "may".** Issue forms from the reference templates, which set the type and `needs: triage`. Discussions switched on. A project board. Local labels for whatever the repository needs. A triage routine. A repository that adopts none of them is in good standing.

**A small package** has nothing to do. **A large repository** keeps its local labels, its scope labels, its stale automation and its backport bot; it gains the first-response view and the outlet for ideas.

**A new repository has nothing to do either.** It arrives with the labels, the forms and the types, because every mechanism sits at the organization level:

- The organization's *default labels for new repositories* are the shared set.
- The organization-level issue templates in `plone/.github` apply to every repository without its own.
- Issue types and issue fields are organization-level by nature.
- A scheduled check in `plone/plone.github` runs the definitions against every repository once a month: it creates missing shared labels, reports deviations, and never deletes a repo-local label. It also catches repositories transferred into the organization, which the default labels miss. The 2015 tool had no such schedule; that is how the drift happened.
- Discussions remain a per-repository choice.
