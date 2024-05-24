.PHONY: test requirements.txt tags

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

test: ruff
	python3 -m unittest discover $(mkfile_dir)/tests "*_test.py"

pylint:
	pylint --disable=C0114,C0115,C0116,R0902,R0401 server.py comfospot40/*.py

ruff: black
	ruff *.py tests/*.py comfospot40/*.py

black:
	black *.py tests/*.py comfospot40/*.py

requirements.txt:
	pip freeze --exclude black --exclude parameterized > requirements.txt

requirements_dev.txt:
	pip freeze > requirements_dev.txt

tags:
	ctags -R --fields=+l --languages=python
