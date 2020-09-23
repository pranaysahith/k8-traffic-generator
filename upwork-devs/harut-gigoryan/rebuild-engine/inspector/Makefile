image-name="ggrig/k8-traffic:re_inspector"

build:
	docker build -t $(image-name) .

run:
	docker run -d $(image-name)

tag:
	docker tag ggrig/k8-traffic ggrig/k8-traffic:re_inspector	

push:
	docker push ggrig/k8-traffic:re_inspector
