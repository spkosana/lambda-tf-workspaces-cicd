.ONESHELL:
.SHELL := /bin/bash
.PHONY: ALL
.DEFAULT_GOAL := ps
VERSION?=latest

ps: # List all the docker compose processes 
	docker compose ps
up: # spinks up the docker containers
	docker compose -f docker-compose.yaml up --build --remove-orphans -d
down: # tear down of docker containes
	docker compose -f docker-compose.yaml down
restart: down up
build: # make build VERSION=1 if no VERSION then creates with Default
	docker buildx build --platform linux/arm64 --provenance=false -t spkosana/lambda-custom:$(VERSION) -f src/Dockerfile src
cov:
	pytest --cov=. --cov-report=term-missing src/tests/test_* --cov-fail-under=100
tests:
	pytest -vvv -s src/tests/test_*.py 
pylint:
	pylint src/*/*.py