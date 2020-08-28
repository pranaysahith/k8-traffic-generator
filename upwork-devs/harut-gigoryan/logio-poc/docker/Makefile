image-name="ggrig/k8-traffic"

build:
	docker build -t $(image-name) .

run:
	docker run -p 8080:16688 -d $(image-name)

tag:
	docker tag ggrig/k8-traffic ggrig/k8-traffic:logio-v2

push:
	docker push ggrig/k8-traffic:logio-v2
