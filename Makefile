#!make
APP_HOST ?= 0.0.0.0
APP_PORT ?= 8080
EXTERNAL_APP_PORT ?= ${APP_PORT}
LOG_LEVEL ?= warning

run = docker-compose run --rm \
				-p ${EXTERNAL_APP_PORT}:${APP_PORT} \
				-e APP_HOST=${APP_HOST} \
				-e APP_PORT=${APP_PORT} \
				app

.PHONY: image
image:
	docker-compose build

.PHONY: docker-run
docker-run: image
	docker-compose up

.PHONY: docker-shell
docker-shell:
	$(run) /bin/bash

.PHONY: run-database
run-database:
	docker-compose run --rm database

.PHONY: pgstac
run-pgstac:
	docker-compose run --rm pgstac
