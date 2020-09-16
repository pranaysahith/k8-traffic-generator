image-name="ggrig/k8-traffic:python"

build:
	docker build -t $(image-name) .

run:
	docker run -d $(image-name)

tag:
	docker tag ggrig/k8-traffic ggrig/k8-traffic:python	

push:
	docker push ggrig/k8-traffic:python
