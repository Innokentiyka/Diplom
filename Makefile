run:
	docker compose --env-file .env up --build -d
dev:
	docker compose --env-file .env up --build
stop:
	docker compose stop
