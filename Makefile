setup:
	docker build . -t vending_machine
	docker compose up -d
	docker compose run web alembic upgrade head

start-server:
	docker compose up -d
	docker logs vending_machine-web-1 -f

stop-server:
	docker compose down -v

clean-up:
	docker compose down -v
