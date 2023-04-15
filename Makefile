GEN_DOC_FOR := \
	pycli.app \
	pycli.command \
	pycli.option \
	pycli.values


all: unit-test lint gen-docs


.PHONY: unit-test
unit-test: ## Run unit testing
	pytest tests/ -v

.PHONY: lint
lint:
	flake8 pycli/

.PHONY: api-docs
gen-docs: ## Generate doc from docstirngs
	python hack/genpydoc.py docs/api ${GEN_DOC_FOR}

