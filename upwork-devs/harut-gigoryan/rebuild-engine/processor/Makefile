image-name="ggrig/k8-traffic:re_processor"

build:
	docker build -t $(image-name) .

run:
	docker run -d $(image-name)

tag:
	docker tag ggrig/k8-traffic ggrig/k8-traffic:re_processor	

push:
	docker push ggrig/k8-traffic:re_processor
