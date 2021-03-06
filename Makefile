.PHONY: tests

help:
	@echo "  help        prints help"
	@echo "  env         create a development environment using virtualenv with necessary dependencies"
	@echo "  clean       remove all pyc"
	@echo "  test        run tests using nose"

env:
	pip install virtualenv && \
	virtualenv .env && \
	. .env/bin/activate && \
	make eggs

eggs:
	pip install -r eggs.txt;
	python nltk_setup.py

clean:
	find . -name '*.pyc' -exec rm -f {} \;

tests:
	make eggs && \
	make clean && \
	nosetests -s
