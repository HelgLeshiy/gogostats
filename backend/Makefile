build:
	docker build -t gogo-backend .
run:
	docker run -d -p 5997:5997 --name gogo-backend gogo-backend
restart:
	docker stop gogo-backend
	docker rm gogo-backend
	docker run -d -p 5997:5997 --name gogo-backend gogo-backend
