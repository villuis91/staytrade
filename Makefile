# docker compose command may be with or without hyphen depending on your version
DOCKER_COMPOSE_COMMAND := $(shell docker compose version > /dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

start: ## Start the docker containers
	@echo "Starting the docker containers"
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml up --remove-orphans
	@echo "Containers started - http://localhost:8000"

stop: ## Stop Containers
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.docker-compose.local.yml down

restart: stop start ## Restart Containers

start-bg:  ## Run containers in the background
	@echo "Starting the docker containers"
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.docker-compose.local.yml up -d
	@echo "Containers started - http://localhost:8000"

build: ## Build Containers
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml build

ssh-django: ## SSH into running web container
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django bash

migrations: ## Create DB migrations in the container
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django python manage.py makemigrations

merge-migrations:
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django python manage.py makemigrations --merge

superadmin: ## Create a super user in django db
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django python manage.py createsuperuser

migrate: ## Run DB migrations in the container
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django python manage.py migrate

translations:
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django python manage.py makemessages --all --ignore node_modules --ignore venv
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django python manage.py makemessages -d djangojs --all --ignore node_modules --ignore venv
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django python manage.py compilemessages

shell: ## Get a Django shell
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django python manage.py shell

pytest: ## Run Django tests
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django pytest

purge-celery: ## purge queue
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django celery -A config.celery_app purge

app: ## Create a super user in django db
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django python manage.py startapp $(name)

release: ## Create a release
	git flow release start $(version)
	git flow release finish $(version)

init: start-bg migrations migrate  ## Quickly get up and running (start containers and migrate DB)

.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

statics:
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django python manage.py collectstatic

test:
	@docker compose -f docker-compose.local.yml run --rm django pytest -v

coverage:
	@$(DOCKER_COMPOSE_COMMAND) -f docker-compose.local.yml run --rm django sh -c "coverage run --source='.' -m pytest -W ignore . ; coverage html"
