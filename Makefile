.PHONY: docs
docs: ## Generate doc from docstirngs
	python hack/genpydoc.py docs/content pycli.app pycli.command pycli.option

.PHONY: lint
lint:
	pylint pycli/

.PHONY: unit-test
unit-testing: ## Run unit testing
	pytest tests/ -v