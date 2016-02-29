PACKAGE=bluecanary

all: install

install:
	python setup.py install

develop:
	pip install -r requirements-dev.txt

lint:
	flake8 $(PACKAGE)

test:
	nosetests

test-with-coverage:
	nosetests --with-coverage --cover-package=$(PACKAGE)

coverage: test-with-coverage

version-patch:
	bumpversion patch setup.py bluecanary/scripts/bluecanary.py

version-minor:
	bumpversion minor setup.py bluecanary/scripts/bluecanary.py

version-major:
	bumpversion major setup.py bluecanary/scripts/bluecanary.py
