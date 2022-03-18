install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:
	yapf -i --style pep8 *.py
lint:
	for i in *.py; do pylint --disable=R,C -sy $$i; done
test:
	pytest -v --cov=. *.py --cov-report xml:reports/coverage/coverage.xml
badge:
	genbadge coverage
git:
	git config --local user.email "aurel.pere@gmail.com"
	git config --local user.name "aurelpere"
	git add coverage-badge.svg
	git commit -m "Updating the test coverage badge"
all: install format lint test 