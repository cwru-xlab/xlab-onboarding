up:
	@docker-compose up --detach --build
	@docker image prune --force

stop:
	@docker-compose stop

down:
	@docker-compose down

clean:
	@docker system prune --all --force