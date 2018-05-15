APP_NAME=journals
NODE_BIN=./node_modules/.bin
TEST_ROOT=test_root
MIN_COVERAGE=40
SELENIUM_BROWSER ?= firefox
SELENIUM_HOST ?= edx.devstack.firefox
JS_TEST_BROWSER ?= FirefoxDocker
JS_TEST_HOST ?= journals.app
.DEFAULT_GOAL := test

.PHONY: clean compile_translations dummy_translations extract_translations fake_translations help html_coverage \
	migrate pull_translations push_translations quality requirements requirements.js prod-requirements \
	test test_python test_js e2e html_coverage quality_python quality_js update_translations validate

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean                      delete generated byte code and coverage reports and test data"
	@echo "  compile_translations       compile translation files, outputting .po files for each supported language"
	@echo "  dummy_translations         generate dummy translation (.po) files"
	@echo "  extract_translations       extract strings to be translated, outputting .mo files"
	@echo "  fake_translations          generate and compile dummy translation files"
	@echo "  help                       display this help message"
	@echo "  html_coverage              generate and view HTML coverage report"
	@echo "  migrate                    apply database migrations"
	@echo "  production-requirements          install requirements for production"
	@echo "  pull_translations          pull translations from Transifex"
	@echo "  push_translations          push source translation files (.po) from Transifex"
	@echo "  quality                    run PEP8 and Pylint and eslint"
	@echo "  quality_python             run PEP8 and Pylint"
	@echo "  quality_js                 run eslint"
	@echo "  requirements               install requirements for local development"
	@echo "  test_python                run python unit tests and generate coverage report"
	@echo "  test_js                    run javascript unit tests and generate coverage report"
	@echo "  test_js_dev                run javascript unit tests in development/debug mode and generate coverage report"
	@echo "  e2e                        run end to end tests"
	@echo "  test                       run tests and generate coverage report"
	@echo "  validate                   run tests and quality checks"
	@echo "  start-devstack             run a local development copy of the server"
	@echo "  open-devstack              open a shell on the server started by start-devstack"
	@echo "  pkg-devstack               build the journals image from the latest configuration and code"
	@echo "  detect_changed_source_translations       check if translation files are up-to-date"
	@echo "  validate_translations      install fake translations and check if translation files are up-to-date"
	@echo ""

clean:
	find . -name '*.pyc' -delete
	coverage erase
	rm -rf coverage $(TEST_ROOT)
	mkdir -p $(TEST_ROOT)/reports

requirements.js:
	npm install

requirements: requirements.js
	pip install -qr requirements/local.txt --exists-action w

production-requirements:
	pip install -qr requirements.txt --exists-action w

test_python: clean
	py.test --cov-config .coveragerc --cov-report term-missing:skip-covered --cov=$(APP_NAME) --ignore=e2e --cov-fail-under=$(MIN_COVERAGE) --rootdir=$(TEST_ROOT)

ifeq ($(CI_ENVIRONMENT), 1)
e2e:
	$(info Skipping e2e tests in continuous integration environment)
else
e2e:
	py.test e2e --driver Remote --junitxml=test_root/reports/e2e/xunit.xml --rootdir=$(TEST_ROOT)
endif

test_js:
	$(NODE_BIN)/gulp test --browsers $(JS_TEST_BROWSER) --hostname $(JS_TEST_HOST) --single-run=true

test_js_dev:
	$(NODE_BIN)/gulp test --browsers $(JS_TEST_BROWSER) --hostname $(JS_TEST_HOST) --single-run=false

test: test_python test_js e2e

quality_python:
	pycodestyle --config=.pycodestyle journals *.py
	pylint --rcfile=pylintrc journals *.py

quality_js:
	$(NODE_BIN)/gulp lint

quality: quality_python quality_js

validate: test quality

migrate:
	python manage.py migrate

html_coverage:
	py.test --cov-config .coveragerc --cov-report html --cov=$(APP_NAME) --rootdir=$(TEST_ROOT)

extract_translations:
	python manage.py makemessages -l en -v1 -d django
	python manage.py makemessages -l en -v1 -d djangojs

dummy_translations:
	cd journals && i18n_tool dummy

compile_translations:
	python manage.py compilemessages

fake_translations: extract_translations dummy_translations compile_translations

pull_translations:
	tx pull -af --mode reviewed

push_translations:
	tx push -s

detect_changed_source_translations:
	cd journals && i18n_tool changed

validate_translations: fake_translations detect_changed_source_translations

# Docker commands below

dev.provision:
	bash ./provision-journals.sh

dev.init: dev.up dev.migrate dev.update_index

dev.update_index:
	docker exec -it journals.app bash -c 'cd /edx/app/journals/journals && python manage.py update_index'

dev.makemigrations:
	docker exec -it journals.app bash -c 'cd /edx/app/journals/journals && python manage.py makemigrations'

dev.migrate: # Migrates databases. Application and DB server must be up for this to work.
	docker exec -it journals.app bash -c 'cd /edx/app/journals/journals && make migrate'

dev.up: # Starts all containers
	docker-compose up -d --build

dev.down: # Kills containers and all of their data that isn't in volumes
	docker-compose down

dev.destroy: dev.down #Kills containers and destroys volumnes
	docker volume rm journals_journals_mysql
	docker volume rm journals_journals_es

dev.stop: # Stops containers so they can be restarted
	docker-compose stop

%-shell: ## Run a shell on the specified service container
	docker exec -it journals.$* bash

%-logs: ## View the logs of the specified service container
	docker-compose logs -f --tail=500 $*

