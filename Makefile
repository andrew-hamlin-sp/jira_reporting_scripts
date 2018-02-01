# Makefile: build issueHistory.py
# Uses python virtualenv, see also:
# http://docs.python-guide.org/en/latest/dev/virtualenvs/

all:
	@echo "Run from virtualenv"
	@echo "$$ source bin/activate"
	@echo "$$ make init"
	@echo "$$ make test"
	@echo "$$ deactivate"

test-all:
	source bin/activate && $(MAKE) test && deactivate
	pushd .py3 && source bin/activate && $(MAKE) test && deactivate && popd

init: 
	python setup.py develop

clean:
	rm -fr build qjira.egg-info
	cd qjira && rm -fr __pycache__ && rm -f *.pyc
	cd tests && rm -fr __pycache__ && rm -f *.pyc
test:
	python setup.py build test

dist:
	python setup.py bdist

dist-all:
	python setup.py sdist

install:
	@echo run setuptools


.PHONY: all init clean test install dist dist-all
