up:
	docker-compose up --build

down:
	docker-compose down --volumes

recompose: down up