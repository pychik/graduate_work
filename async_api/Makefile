lint:
	isort ./src && flake8 ./src
	isort ./tests && flake8 ./tests
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
test:
	docker-compose -f docker-compose-tests.yml up