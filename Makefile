# Build the Plone GitHub issue-process proposal.
#   make test      run the test suite
#   make data      re-fetch the audit data from GitHub (needs `gh auth login`)
#   make pdf       build build/proposal.pdf (numbers → diagrams → markdown → pandoc)
UV ?= uv

.PHONY: test data numbers diagrams md pdf clean

test:
	$(UV) run pytest

data numbers diagrams md pdf:
	@echo "$@: not implemented yet" >&2; exit 1

clean:
	rm -rf build
