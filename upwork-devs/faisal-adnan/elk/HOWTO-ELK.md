## ELK Quick Start 
Running ELK Stack on Minikube
### Start minikube
```
    minikube start --driver=virtualbox
```
### Create ECK operator
```
    kubectl apply -f https://download.elastic.co/downloads/eck/1.2.1/all-in-one.yaml
    kubectl -n elastic-system logs -f statefulset.apps/elastic-operator
```
### Deploy ELK. This may take 5+ minutes.
```
    kubectl apply -f elk/tenant.yml
```
### Open Kibana on http://localhost:5601
```
    kubectl port-forward service/quickstart-kb-http 5601
```
### Add filebeat-* to the Index Pattern 
### Continue with load testing