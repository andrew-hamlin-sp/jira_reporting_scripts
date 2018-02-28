# Makefile: build issueHistory.py
# Uses python virtualenv, see also:
# http://docs.python-guide.org/en/latest/dev/virtualenvs/

all:
	@echo "Run from virtualenv"
	@echo "$$ source bin/activate"
	@echo "$$ make init"
	@echo "$$ make test"
	@echo "$$ deactivate"

_py27:
	virtualenv --python=python2.7 _py27
	cd _py27 && ln -s ../Makefile ../setup.py ../qjira ../tests .

_py3:
	virtualenv --python=python3 _py3
	cd _py3 && ln -s ../Makefile ../setup.py ../qjira ../tests .

test-all: _py27 _py3
	pushd _py27 && source bin/activate && $(MAKE) test && deactivate && popd
	pushd _py3 && source bin/activate && $(MAKE) test && deactivate && popd

init: 
	python setup.py develop

clean:
	rm -fr build qjira.egg-info
	cd qjira && rm -fr __pycache__ && rm -f *.pyc
	cd tests && rm -fr __pycache__ && rm -f *.pyc

clean-all: clean
	rm -fr _py27
	rm -fr _py3

test:
	python setup.py build test

dist:
	python setup.py bdist

dist-all:
	python setup.py sdist

install:
	@echo run setuptools


.PHONY: all init clean clean-all test test-all install dist dist-all
