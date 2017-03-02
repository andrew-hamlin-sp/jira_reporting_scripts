# Makefile: build issueHistory.py

all:
	@echo "issueHistory.py build"

prepare: requirements.txt
	pip install -r requirements.txt

test:
	@echo "Run tests"

.PHONY:
