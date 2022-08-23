VENV = .env
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

$(VENV)/bin/activate: requirements.txt
	python3 -m venv .env
	$(PIP) install -r requirements.txt

build_api:
	docker compose build api

populate_database:
	docker exec cheese_database /bin/sh -c 'chmod +x /run/init/initialize_database.sh && ./run/init/initialize_database.sh'

up:
	docker compose up -d

down:
	docker compose down

help:
	@echo "Usage & commands list:"
	@echo "	* [make] to create venv and install libraries"
	@echo "	* [make build_api] to build flask docker image"
	@echo "	* [make populate_database] to load data into database"
	@echo "	* [make up] to run project"
	@echo "	* [make down] to stop"

