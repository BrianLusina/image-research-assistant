# define standard colors
ifneq (,$(findstring xterm,${TERM}))
	BLACK        := $(shell tput -Txterm setaf 0)
	RED          := $(shell tput -Txterm setaf 1)
	GREEN        := $(shell tput -Txterm setaf 2)
	YELLOW       := $(shell tput -Txterm setaf 3)
	LIGHTPURPLE  := $(shell tput -Txterm setaf 4)
	PURPLE       := $(shell tput -Txterm setaf 5)
	BLUE         := $(shell tput -Txterm setaf 6)
	WHITE        := $(shell tput -Txterm setaf 7)
	RESET := $(shell tput -Txterm sgr0)
else
	BLACK        := ""
	RED          := ""
	GREEN        := ""
	YELLOW       := ""
	LIGHTPURPLE  := ""
	PURPLE       := ""
	BLUE         := ""
	WHITE        := ""
	RESET        := ""
endif

.PHONY: help
help: ## describe all commands
	@grep -E '^[a-zA-Z_]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Installs dependencies
	uv install -r pyproject.toml

.PHONY: setup
setup: ## Create virtualenv and install dependencies
	python3 -m venv .venv
	. .venv/bin/activate && $(MAKE) install

PORT ?= 8000

.PHONY: run
run: ## Runs application
	cd src && python app/main.py

.PHONY: test
test: ## Runs tests
	uv run pytest -vv -s -o log_cli=true -o log_cli_level=DEBUG -o cache_dir=/tmp tests/$(test)

.PHONY: test-cover
test-cover: ## Runs tests with coverage
	uv run coverage run --source='./src/' -m pytest -v --junitxml junit-report.xml tests/ && coverage xml && coverage report -m

.PHONY: ruff
ruff: ## lints project using ruff
	uv run ruff format .

.PHONY: fix-ruff
fix-ruff: ## Runs check with ruff & fixes files
	uv run ruff check --fix .

.PHONY: pyrefly
pyrefly: ## Runs type checks with pyrefly
	uv run pyrefly check

.PHONY: lint
lint: ruff pyrefly

.PHONY: clean
clean: ## removes dist folder
	rm -rf dist

.PHONY: build
build: ## builds project
	uv build

.PHONY: publish-gitlab
publish-gitlab: build ## publish python package to Gitlab package registry
	TWINE_PASSWORD=${CI_JOB_TOKEN} TWINE_USERNAME=gitlab-ci-token uv run twine upload --repository-url ${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/packages/pypi dist/*

.PHONY: publish-pypi
publish-pypi: build ## publish python package to PyPI
	uv run twine upload --verbose -u '__token__' dist/*