up:
	@docker-compose up -d --build
	@docker image prune --force

stop:
	@docker-compose stop

down:
	@docker-compose down