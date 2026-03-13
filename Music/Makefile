# ==========================
# Python Project Makefile
# Project: a-maze-ing.py
# ==========================

PYTHON = python3
MAIN = a_maze_ing.py

# Default target
all: run
CONFIG = config.txt

# Install project dependencies
install:
	@pip install -r requirements.txt > /dev/null

# Run the project
run:
	@if [ -z "$(CONFIG)" ]; then \
		echo "Error: No config .txt file found."; \
	fi
	@$(PYTHON) $(MAIN) $(CONFIG)

# Debug mode
debug:
	@if [ -z "$(CONFIG)" ]; then \
		echo "Error: No config .txt file found."; \
	fi
	@$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# Lint code
lint:
	@$(PYTHON) -m flake8 . > /dev/null
	@$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Strict lint (optional/recommended)
lint-strict:
	@$(PYTHON) -m flake8 .
	@$(PYTHON) -m mypy . --strict

# Build the project
build:
	@$(PYTHON) -m pip install --quiet --upgrade build > /dev/null
	@$(PYTHON) -m build > /dev/null
	@cp dist/mazegen-*.whl . 2>/dev/null || true
	@cp dist/mazegen-*.tar.gz . 2>/dev/null || true

# Clean python cache files
clean:
	@find . -type d -name "__pycache__" -exec rm -r {} + > /dev/null 2>&1
	@find . -type d -name ".mypy_cache" -exec rm -r {} + > /dev/null 2>&1
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "*.egg-info" -exec rm -r {} + > /dev/null 2>&1
	@rm -rf dist/ build/

.PHONY: all install run debug lint lint-strict clean build