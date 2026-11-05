# The shared label set

These eight labels become the organization's default label set. They are created centrally in every repository; using them is optional.

| Label | Meaning | Set by | Removed by |
|-------|------------|---------|-------------|
| `needs: triage` | New, nobody has looked yet | The issue form, automatically | Whoever takes the first look: keep as issue, convert to Discussion, close with a reason, or ask the reporter |
| `needs: info` | Waiting for the reporter; an answer is expected within thirty days | A maintainer, with a comment saying what is needed and by when | When the reporter answers. After the window without an answer the issue may be closed as *not planned*, with an invitation to reopen by replying |
| `help wanted` | Maintainers will not drive this; contributions welcome | A maintainer | — |
| `good first issue` | Small, well scoped, friendly to a newcomer | A maintainer | — |
| `blocker` | Blocks a release or stops other work; the one alarm everybody must see at a glance, on issues and PRs alike | A release manager or maintainer | When resolved |
| `accessibility` | Accessibility concern, followed across repositories by the accessibility team | Anyone | — |
| `i18n` | Internationalization or localization concern, followed across repositories | Anyone | — |
| `documentation` | Documentation concern, followed across repositories by the documentation team | Anyone | — |

A few notes on the set:

- `help wanted` and `good first issue` use GitHub's exact names and GitHub's standard colours, so the repository's *Contribute* page and the newcomer discovery work again.
- **Confirmed is not a label.** In a repository that applies `needs: triage` on creation, its absence means that someone has looked. In a repository that does not, the label is simply not in use, and its absence means nothing.
- **`needs: info` has a clock.** A reporter can be expected to answer within a defined time; thirty days is the default, chosen for a volunteer community, and a team may shorten or lengthen it. The expectation is stated twice, in the label description and in the comment the maintainer leaves. How a team acts on the clock is its own choice (section 7).
- **Priority is a field, not a label.** Graded priority (Urgent, High, Medium, Low) is the organization's Priority issue field, switched to public visibility. It is set after creation by whoever triages, since issue forms cannot preset field values, and priority is a triage decision anyway. The Effort field (High, Medium, Low) takes over what the old `lvl:` labels tried to express.
- **`blocker` is rare by design.** Its low usage is what the word means. It stays a label although the Priority field has an *Urgent* option, because a blocker must be visible to everybody at a glance, including on pull requests and to scripts.
- **Colours**: one hue for the two `needs:` labels, dark red for `blocker`, one hue for the three concern labels, GitHub's defaults for the two GitHub labels.
