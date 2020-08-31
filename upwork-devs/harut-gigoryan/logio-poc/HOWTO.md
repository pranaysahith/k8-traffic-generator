# POC with logio.org as a log monitoring tool 
Running the test:
## Install minikube
Follow the minibuke installation instruction for your OS
https://kubernetes.io/docs/tasks/tools/install-minikube/
## Start minikube
```
    minikube start --driver=virtualbox
```
## Deploy logio
```
    kubectl apply -f logio-deployment.yaml
```
## Start the service
```
    kubectl apply -f logio-service.yaml
```
## Get it in the browser
```
    minikube service logio
```