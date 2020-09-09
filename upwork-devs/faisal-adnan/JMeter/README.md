# JMeter PoC
Create a pod that executes a recorded script test using JMeter
# Prerequisites
## Mac OSX
### Install minikube
```
    brew install minikube
```
# Quick Start
Running load test using JMeter against website glasswallsolutions.com
## Start minikube
```
    minikube start --driver=virtualbox --cpus 3 --memory 8192
```
## Deploy ELK and Minio
See folder elk and Minio
## Deploy artillery as a job
```
    sh run.sh <jmx_file> <number_of_pods>
```