.PHONY: start, stop

start:
	docker-compose -f ./docker-compose.yml up --build -d

stop:
	docker-compose -f ./docker-compose.yml down --rmi local
