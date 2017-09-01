# Makefile: build issueHistory.py
# Uses python virtualenv, see also:
# http://docs.python-guide.org/en/latest/dev/virtualenvs/

all:
	@echo "Run from virtualenv"
	@echo "$$ source bin/activate"
	@echo "$$ make init"
	@echo "$$ make test"
	@echo "$$ deactivate"

init: 
#	pip install -r requirements.txt
	python setup.py develop

clean:
	cd qjira && rm -fr __pycache__ && rm -f *.pyc
	cd tests && rm -fr __pycache__ && rm -f *.pyc
test:
	python setup.py test

install:
	@echo run setuptools


.PHONY: all init test install
