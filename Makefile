.PHONY: test requirements.txt

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

test:
	python3 -m unittest discover $(mkfile_dir)/tests "*_test.py"
black:
	black *.py tests/*.py comfospot40/*.py

requirements.txt:
	pip freeze --exclude black --exclude parameterized > requirements.txt

requirements_dev.txt:
	pip freeze > requirements_dev.txt
