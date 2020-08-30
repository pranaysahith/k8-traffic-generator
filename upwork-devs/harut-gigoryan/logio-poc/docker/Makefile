image-name="ggrig/k8-traffic"

build:
	docker build -t $(image-name) .

run:
	docker run -p 16688:16688 -p 16689:16689 -d $(image-name)

tag:
	docker tag ggrig/k8-traffic ggrig/k8-traffic:logio-v2

push:
	docker push ggrig/k8-traffic:logio-v2
