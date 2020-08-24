# Quick Start 
Running testing with the following flow:
- Open https://glasswallsolutions.com/technology
- Open https://glasswallsolutions.com/products
- Open https://glasswallsolutions.com/pricing
- Open https://glasswallsolutions.com/resources
- Open https://glasswallsolutions.com/company
## Install minikube
```
    brew install minikube
```
## Start minikube
```
    minikube start --driver=virtualbox
```
## Deploy artillery
```
    kubectl apply -f artillery.yaml
```
# Customising Test Flow
## Edit load.yml
## Build docker file
```
    docker build -t <DOCKER_HUB_ACCOUNT>/<IMAGE_NAME>:<VERSION> -f Dockerfile 
```
## Push image to Docker Hub
```
    docker login --username=<DOCKER_HUB_ACCOUNT>
    docker push <DOCKER_HUB_ACCOUNT>/<IMAGE_NAME>:<VERSION>
```
## Deploy to k8s again
### Change image name in artillery.yaml to <DOCKER_HUB_ACCOUNT>/<IMAGE_NAME>:<VERSION>
### Deploy with kubectl
