.DEFAULT_GOAL := help

# determines what "make help" will show
define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

.PHONY: help build test serve

help: ## Show what this Makefile can do
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

validate_cff: CITATION.cff ## Makes sure the CITATION.cff file is valid. (pip install cffconvert)
	cffconvert --validate

test: ## Build the book, checks for dead link and fail on warning
	jupyter-book build specification --warningiserror --builder linkcheck

html: ## Build html version of the book
	jupyter-book build specification

serve: html ## Serve the built website
	python -m http.server -d specification/_build/html/

pdfhtml: ## Build pdf version of the book from html (requires pyppeteer)
	jupyter-book build specification --builder pdfhtml

pdflatex: ## Build pdf version of the book from latex
	jb build specification --builder pdflatex 

