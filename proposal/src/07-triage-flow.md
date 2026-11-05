# The triage flow

![From a new issue to a decision](build/diagrams/triage-flow.pdf){width=100%}

A new issue arrives through the form, typed and marked `needs: triage`. Whoever triages in that repository takes a first look and does one of four things: converts it to a Discussion, closes it with a reason, asks the reporter and adds `needs: info`, or accepts it and removes `needs: triage`. On acceptance a Priority, a milestone, a board or a concern label may follow; none of them must. From there the work is the usual one: assignee, draft pull request, checks, review, merge, closed as completed.

## How `needs: triage` gets onto an issue

Always automatically, never by hand. The human path is one removal click.

1. **Issue forms.** Volto and Aurora set the label in their own forms today, and the organization-level default templates in `plone/.github` set it for every repository without own forms. They fail silently wherever the label does not exist, which the shared set fixes overnight. The remaining gap, blank issues created without a form, closes with one line in the organization's `config.yml`: `blank_issues_enabled: false`. The comment in that file already anticipates it. Issues created through the API are rare and mostly bots.
2. **A reusable workflow** in the shared workflows of `plone/meta`, for repositories that want the remaining paths covered or want `needs: info` removed automatically when the reporter answers. It needs a small caller workflow per repository, which the existing configuration rollout of `plone/meta` already distributes for the core packages. Optional.

The rollout script never adds `needs: triage` to existing open issues. Only issues created after a repository or the organization switches the mechanism on carry it.

## Two filters for those who triage

- `is:open label:"needs: triage"` lists the issues still waiting for a first response.
- `is:open -label:"needs: triage" -label:"needs: info"` lists those that have had one.

Teams that do not triage lose nothing; the label stays on the issue, which is no worse than today.

## Acting on the `needs: info` clock

The label carries the expectation that a reporter answers within thirty days. Two ways to act on it, both optional:

- *By hand*: a saved filter on `needs: info` and the last update date; close as *not planned* with the standard sentence that a reply reopens the issue.
- *Automated*: the reusable workflow comments at day thirty, closes at day forty-four, removes the label and reopens when the issue author replies. This is deliberately narrower than a stale bot: it only acts on issues where a human explicitly asked for something, so teams that reject automatic closing keep the manual path and the same label.

Removing the label when the author replies is the one piece of automation worth having everywhere. It saves a click, keeps the filter honest, and implies no closing policy.
