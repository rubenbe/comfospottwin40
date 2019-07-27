.PHONY: tests

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(dir $(mkfile_path))

tests:
	python3 -m unittest discover $(mkfile_dir)/tests "*_test.py"
