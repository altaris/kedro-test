DOCS_PATH 		= docs
SRC_PATH 		= src
VENV			= ./venv
PDOC			= python3 -m pdoc -d google --math

.ONESHELL:

all: format typecheck lint

.PHONY: docs
docs:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	$(PDOC) --output-directory $(DOCS_PATH) $(SRC_PATH)

.PHONY: docs-browser
docs-browser:
	-@mkdir $(DOCS_PATH) > /dev/null 2>&1
	$(PDOC) $(SRC_PATH)

.PHONY: format
format:
	# isort .
	python3 -m black --line-length 79 --target-version py310 $(SRC_PATH)
	python3 -m black --line-length 79 --target-version py310 *.py

.PHONY: lint
lint:
	python3 -m pylint $(SRC_PATH)

.PHONY: typecheck
typecheck:
	python3 -m mypy -p $(SRC_PATH)
	python3 -m mypy *.py
