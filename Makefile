.PHONY: test

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

test:
	python3 -m unittest discover $(mkfile_dir)/tests "*_test.py"
black:
	black *.py tests/*.py comfospot40/*.py
