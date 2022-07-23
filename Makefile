PROJECT_NAME ?= vpnbot
VERSION = $(shell python3 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= tr30012
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

PG_DB ?= $(PROJECT_NAME)
PG_USER ?= $(PROJECT_NAMESPACE)
PG_PASSWORD ?= hackme

all:
	@echo "make postgres		- Start postgres container"
	@echo "make build           - Build vpnbot docker image"
	@echo "make vpnbot          - Run vpnbot image"
	@exit 0

postgres:
	docker stop vpnbot-postgres || true
	docker run --rm --detach --name=vpnbot-postgres \
		--env POSTGRES_USER=$(PG_USER) \
		--env POSTGRES_PASSWORD=$(PG_PASSWORD) \
		--env POSTGRES_DB=$(PG_DB) \
		--env PGDATA=/var/lib/postgresql/data/pgdata \
		-v ./pgdata:/var/lib/postgresql/data \
		--publish 5432:5432 postgres

build:
	docker build -t $(PROJECT_NAME):$(VERSION) .


vpnbot:
	docker stop vpnbot || true
	docker run --rm --detach --name=vpnbot \
		--env POSTGRES_USER=$(PG_USER) \
		--env POSTGRES_PASSWORD=h$(PG_PASSWORD) \
		--env POSTGRES_DB=$(PG_DB) \
		--publish 8000:8000 \
		$(PROJECT_NAME):$(VERSION)
