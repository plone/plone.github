# Rollout and how to give feedback

Nothing here is formal. The steps are the ones Plone has used for changes like this before.

1. **Feedback.** This proposal is posted on community.plone.org and announced on Discord. For about four weeks, team leads, release managers and active contributors are asked for their view, directly if they stay silent. The documentation team is asked early: the rollout touches the contributing documentation, and the "How we handle issues" section the Volto team is writing is where its own practice and this proposal meet.
2. **Decision.** A PLIP-style issue in `plone/plone.github` with a seconder; +1s from the people above; no opponents.
3. **Scripted rollout** by the organization admin: set the default labels; run the migration in dry-run mode and read the report; check the auto-add workflows of the active boards against it; set the Priority and Effort fields to public; run the migration; update the organization-level templates in `plone/.github`; switch on the monthly check; update the contributing documentation.
4. **Teams adopt** Discussions, forms and boards at their own pace.

**How the migration treats each old label.** Every label of the 2015 scheme falls into one of three classes, listed in Appendix A. *Rename*: the successor is the same label under a new name; existing issues keep it. *Move to a native field*: the script sets the issue type or the Priority field and removes the label; nothing is lost, the fact moves. *Retire*: the label definition is deleted where it sits on no item at all, and archived where it is still in use, so that history stays and the team can bring it back with one click. Labels not listed in Appendix A are never touched.

**What this proposal does not do.** It does not clean up existing issues. Whether and how a team goes through its open issues is the team's decision and a separate conversation.

**Give feedback** in the forum thread, on Discord, or as an issue or pull request in `plone/plone.github`, where the data behind every number in this document lives and can be re-run.
