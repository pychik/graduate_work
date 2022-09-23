lint:
	isort ./app && flake8 ./app
up:
	docker-compose -f docker-compose.yml up -d
down:
	docker-compose -f docker-compose.yml down
stop:
	docker-compose -f docker-compose.yml stop
build:
	docker-compose -f docker-compose.yml up -d --build
rebuild:
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose.yml up -d --build
rebuild_app:
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose.yml up -d --build app
test:
	docker-compose -f docker-compose-tests.yml up