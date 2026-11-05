# Build the Plone GitHub issue-process proposal.
#   make test      run the test suite
#   make data      re-fetch the audit data from GitHub (needs `gh auth login`)
#   make pdf       build build/proposal.pdf (numbers → diagrams → markdown → pandoc)
UV ?= uv

.PHONY: test data numbers diagrams md pdf clean

test:
	$(UV) run pytest

data:
	$(UV) run python -m scripts.fetch_labels
	$(UV) run python -m scripts.usage
	$(UV) run python -m scripts.extra_usage
	$(UV) run python -m scripts.projects_probe
	$(UV) run python -m scripts.features_probe

numbers:
	$(UV) run python -m scripts.numbers

diagrams:
	mkdir -p build/diagrams
	for f in proposal/diagrams/*.dot; do dot -Tpdf -o build/diagrams/$$(basename $$f .dot).pdf $$f; done

md: numbers
	$(UV) run python -m scripts.render

pdf: numbers diagrams md
	pandoc build/proposal.md --defaults proposal/template/defaults.yaml -o build/proposal.pdf

clean:
	rm -rf build
