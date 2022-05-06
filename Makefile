.PHONY: build test serve

build:
	jb build specification

test:
	jb build specification -W --builder linkcheck

serve: build
	python -m http.server -d specification/_build/html/
