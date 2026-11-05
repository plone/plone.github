# plone.github

Definitions, data and the 2026 proposal for how repositories in the
[Plone GitHub organization](https://github.com/plone) handle issues and labels.

In 2015 this repository held the tool that rolled out a numbered label
scheme across the organization. That tool and the Google Sheet that
documented the scheme are kept under [`archive/`](archive/). Everything else
here belongs to the 2026 proposal: fewer labels, GitHub's own features for
the rest, and a lighter process for the people who triage.

## Layout

```
archive/        the 2015 tool and the Google Sheet, as they were
data/           audit of every public repository in the org (2026-11-05) and
                the scripts that produced it
proposal/       Markdown sources of the proposal PDF, diagrams, PDF template,
                and the forum post
Makefile        make test | make pdf | make data
```

## Build the PDF

Needs Python 3.12+, [uv](https://docs.astral.sh/uv/), pandoc, XeLaTeX with
the Lato font, Graphviz and poppler-utils. On Debian/Ubuntu:

```
sudo apt-get install pandoc texlive-xetex texlive-latex-extra texlive-fonts-recommended fonts-lato graphviz poppler-utils
uv sync
make pdf          # → build/proposal.pdf
make test
```

## Regenerate the data

`make data` queries the GitHub GraphQL API through the `gh` CLI for every
public repository in the organization and rewrites `data/`. It needs
`gh auth login` with read access to the org and takes about ten minutes.
Private repositories are never read or written.

## Discussion

The proposal is discussed on the Plone community forum: TBD (link added
when posted). Feedback as issues or pull requests here is welcome too.
