# k8-traffic-generator

## To run traffic generator using docker

* Start traffic generator by running `docker-compose up --build`

* Traffic generator is integrated with opencensus for prometheus and the time taken for each action is measured and the metrics are exposed on localhost:8000/metrics

## To run traffic generator on kubernetes

* Setup Prometheus using helm chart - `helm install prometheus stable/prometheus`

* Deploy kubernetes manifest file by running - `kubectl apply -f traffic_generator.yaml`

* Open prometheus UI and query for metrics "glasswall_views_home_page_response_bucket" and "glasswall_views_download_brochure_response_bucket"

* Filter metrics based on TEST_ID to get metrics of specific TEST_ID e.g. glasswall_views_home_page_response_bucket{TEST_ID="1002"}
