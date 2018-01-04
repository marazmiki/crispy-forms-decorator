.PHONY: tox
tox:
	tox --skip-missing-interpreters


.PHONY: test
test:
	PYTHONPATH=. pytest


.PHONY: cov
cov:
	make test
	coverage html


.PHONY: flake8
flake8:
	flake8 .
