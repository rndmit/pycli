.PHONY: docs
docs: ## Generate doc from docstirngs
	python hack/genpydoc.py docs/content pycli.app pycli.command pycli.option

.PHONY: unit-testing
unit-testing: ## Run unit testing
	pytest tests/ -v