.PHONY: start, stop

start:
	docker compose up --build -d

stop:
	docker compose down --rmi local

deploy:
	docker compose up -d

build:
	docker build fakel/ -t jojopko/fakel:latest

