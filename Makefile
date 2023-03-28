.PHONY: docs
docs:
	python hack/genpydoc.py docs/content pycli.app pycli.command pycli.option

.PHONY: docserv
docserv: docs
	hugo server -s ./docs/