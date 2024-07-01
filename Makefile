.PHONY: start-dev, stop-dev

start-dev:
	docker-compose -f ./docker-compose.yml up --build -d

stop-dev:
	docker-compose -f ./docker-compose.yml down --rmi local

start:
	echo 'В разработке'

stop:
	echo 'В разработке'
