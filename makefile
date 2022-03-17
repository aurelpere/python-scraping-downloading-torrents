install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:
	blue *.py
lint:
	for i in *.py; do pylint --disable=R,C -sy $$i; done
test:
	pytest -s --cov=. test_*
all: install format lint test 