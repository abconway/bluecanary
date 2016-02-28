PACKAGE=bluecanary

all: install

install:
	python setup.py install

develop:
	pip install -e .

lint:
	flake8 $(PACKAGE)

test:
	nosetests

test-with-coverage:
	nosetests --with-coverage --cover-package=$(PACKAGE)
