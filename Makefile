PROJECT_NAME ?= vpnbot
VERSION = $(shell python setup.py --version | tr '+' '-')
TOKEN = $(shell python bot_token.py)
PROJECT_NAMESPACE ?= tr30012
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

PG_HOST ?= vpnbot-postgres
PG_DB ?= $(PROJECT_NAME)
PG_USER ?= $(PROJECT_NAMESPACE)
PG_PASSWORD ?= hackme
PG_PORT ?= 5432

DOCKER_NETWORK_NAME ?= postgres-bridge


all:
	@echo "make token           - Show bot token"
	@echo "make clean		    - Remove dist info"
	@echo "make postgres		- Start postgres container"
	@echo "make docker-build    - Build vpnbot docker image"
	@echo "make docker-run      - Run vpnbot image"
	@echo "make install         - Install package locally"
	@echo "make sdist		    - Make source distribution"
	@echo "make build           - Build package in the same dir"
	@echo "make devenv          - Creates python dev environment"
	@echo "make run             - Installs package and runs it locally"
	@exit 0

token:
	@echo $(TOKEN)

clean:
	rm -fr *.egg-info dist build


postgres:
	docker stop vpnbot-postgres || true
	docker network rm $(DOCKER_NETWORK_NAME) || true
	docker network create -d bridge $(DOCKER_NETWORK_NAME)
	docker run --rm --detach --name=vpnbot-postgres \
		--env POSTGRES_USER=$(PG_USER) \
		--env POSTGRES_PASSWORD=$(PG_PASSWORD) \
		--env POSTGRES_DB=$(PG_DB) \
		--env PGDATA=/var/lib/postgresql/data/pgdata \
		-v ./pgdata:/var/lib/postgresql/data \
		--network $(DOCKER_NETWORK_NAME) \
		--publish 5432:5432 --expose 5432 postgres

devenv: clean
	rm -rf env
	python -m venv env

sdist: clean
	python setup.py sdist


docker-build:
	docker build --target=api -t $(PROJECT_NAME):$(VERSION) .


docker-run:
	docker stop $(PROJECT_NAME) || true
	docker run --rm --detach --name=$(PROJECT_NAME) \
		--env POSTGRES_HOST=$(PG_HOST) \
		--env POSTGRES_PORT=$(PG_PORT) \
		--env POSTGRES_USER=$(PG_USER) \
		--env POSTGRES_PASSWORD=$(PG_PASSWORD) \
		--env POSTGRES_DB=$(PG_DB) \
		--env TOKEN=$(TOKEN) \
		--publish 8000:8000 \
		--network=$(DOCKER_NETWORK_NAME) \
		$(PROJECT_NAME):$(VERSION)


install:
	python setup.py install
	rm -fr *.egg-info dist build


build:
	python setup.py build

run: install
	vpnbot-bot $(TOKEN)
