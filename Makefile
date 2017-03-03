# Makefile: build issueHistory.py
# Uses python virtualenv, see also:
# http://docs.python-guide.org/en/latest/dev/virtualenvs/

all:
	@echo "issueHistory.py build"

prepare: requirements.txt
	pip install -r requirements.txt

test:
	@echo "Run tests"

.PHONY:
