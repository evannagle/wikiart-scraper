APP_NAME 					= 	pyboot
BIN_FOR_APP 				= 	$(APP_NAME)/app.py
BIN_FOR_NODE				= 	node
BIN_FOR_NPM					= 	npm
BIN_FOR_NPX 				= 	npx
BIN_FOR_PIP					= 	pip
BIN_FOR_PYTHON				= 	python3
BIN_FOR_POETRY				= 	poetry
PATHS_THAT_ARE_EPHEMERAL 	= 	__pycache__ .pytest_cache .coverage .mypy_cache .tox .eggs .venv
PATH_TO_COVERAGE			= 	htmlcov/index.html
PATH_TO_SCRIPTS				= 	scripts
PATH_TO_DOCSITE				= 	site/index.html

.PHONY: %

define title
	@echo "\n\033[1;33m🤖$(1)\033[0m"
endef

assume:
# Assume the project is set up.
# First, make sure `npm install` has been run.
	@$(BIN_FOR_NPM) list --depth=0 > /dev/null  || (echo "You are missing dependencies. Did you run 'npm install' first?" && exit 1)

huh: assume
# Get the name of the command.
# Print the command, followed by the comments below it, like this one!
	@$(BIN_FOR_NODE) $(PATH_TO_SCRIPTS)/makefile-parser.js --format=list

install:
# Install the project dependencies
	$(call title, Installing the project dependencies)
	$(BIN_FOR_NPM) install
	$(BIN_FOR_POETRY) install
	$(BIN_FOR_NPX) husky init
	echo "make pre-commit" > .husky/pre-commit

clean:
# Remove all the ephemeral files
	$(call title, Cleaning up)
	rm -rf $(PATHS_THAT_ARE_EPHEMERAL)

deep-clean: clean
# Clean up all generated files
# Also clean up the poetry cache
	$(call title, Deep cleaning up)
	$(PATH_TO_SCRIPTS)/deep-clean.sh

build:
# Build the project.
# Ensure the dependencies are installed and the project is ready to run
	$(call title, Building the project)
	$(BIN_FOR_POETRY) install

app: clean build
# Run the app
	$(call title, Running the app)
	$(BIN_FOR_POETRY) run $(APP_NAME)

test: build
# Run the tests
	$(call title, Running tests)
	$(BIN_FOR_POETRY) run coverage run -m pytest

test-coverage: test
# Run the tests with coverage
	$(call title, Running tests with coverage)
	$(BIN_FOR_POETRY) run coverage html
	open $(PATH_TO_COVERAGE)


docs:
	$(call title, Generating the documentation)
	$(BIN_FOR_POETRY) run mkdocs build
.PHONY: docs

site: docs
# Generate the documentation
	$(call title, Opening the documentation site)
	open $(PATH_TO_DOCSITE)
.PHONY: site

format:
# Format the code
	$(call title, Formatting the code)
	$(BIN_FOR_POETRY) run black $(APP_NAME) 

install-husky:
# Install husky if it's not already installed.
	$(call title, "Installing husky if needed")
	@$(BIN_FOR_NPM) install --save-dev husky
	$(BIN_FOR_NPX) husky init

lint: format
# Run the linter
	$(call title, Running the linter)
	$(BIN_FOR_POETRY) run ruff check $(APP_NAME)

lint-fix: format
# Run the linter and fix the issues
	$(call title, Running the linter and fixing the issues)
	$(BIN_FOR_POETRY) run ruff check $(APP_NAME) --fix --no-cache
	
pre-commit: lint-fix test
# Run the pre-commit checks
	$(call title, Running the pre-commit checks)

rename: assume clean
# Rename the project.
	$(call title, "Renaming the project")
	$(BIN_FOR_NODE) $(PATH_TO_SCRIPTS)/rename-project.js

changelog:
# Generate the changelog for the project.
	$(call title, "Generating changelog")
	$(BIN_FOR_POETRY) run towncrier

globalize:
# Globalize the project.
	$(call title, "Globalizing the project")
	$(BIN_FOR_POETRY) env remove --all
	$(BIN_FOR_POETRY) env use $(BIN_FOR_PYTHON)
	$(BIN_FOR_POETRY) install
	$(BIN_FOR_PIP) install --editable .

env:
# Move `.env-example` to `.env`.
	$(call title, "Moving .env-example to .env")
	cp .env-example .env