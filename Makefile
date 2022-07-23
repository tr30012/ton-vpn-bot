PROJECT_NAME ?= vpnbot
VERSION = $(shell python setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= tr30012
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

PG_HOST ?= 0.0.0.0
PG_DB ?= $(PROJECT_NAME)
PG_USER ?= $(PROJECT_NAMESPACE)
PG_PASSWORD ?= hackme


all:
	@echo "make clean		    - Remove dist info"
	@echo "make postgres		- Start postgres container"
	@echo "make docker-build    - Build vpnbot docker image"
	@echo "make docker-run      - Run vpnbot image"
	@echo "make install         - Install package locally"
	@echo "make sdist		    - Make source distribution"
	@echo "make build           - Build package in the same dir"
	@exit 0


clean:
	rm -fr *.egg-info dist build


postgres:
	docker stop vpnbot-postgres || true
	docker run --rm --detach --name=vpnbot-postgres \
		--env POSTGRES_USER=$(PG_USER) \
		--env POSTGRES_PASSWORD=$(PG_PASSWORD) \
		--env POSTGRES_DB=$(PG_DB) \
		--env PGDATA=/var/lib/postgresql/data/pgdata \
		-v ./pgdata:/var/lib/postgresql/data \
		--publish 5432:5432 postgres


sdist: clean
	python setup.py sdist


docker-build: sdist
	docker build --target=api -t $(PROJECT_NAME):$(VERSION) .


docker-run:
	docker stop vpnbot || true
	docker run --rm --detach --name=vpnbot \
		--env POSTGRES_HOST=$(PG_HOST) \
		--env POSTGRES_PORT=$(PG_PORT) \
		--env POSTGRES_USER=$(PG_USER) \
		--env POSTGRES_PASSWORD=h$(PG_PASSWORD) \
		--env POSTGRES_DB=$(PG_DB) \
		--publish 8000:8000 \
		$(PROJECT_NAME):$(VERSION)


install:
	python setup.py install
	rm -fr *.egg-info dist build


build:
	python setup.py build
