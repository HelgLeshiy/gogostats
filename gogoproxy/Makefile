build:
	docker build -t gogoproxy .
run:
	docker run -d -p 5800:5800 --name gogoproxy gogoproxy
restart:
	docker stop gogoproxy
	docker rm gogoproxy
	docker run -d -p 5800:5800 --name gogoproxy gogoproxy
