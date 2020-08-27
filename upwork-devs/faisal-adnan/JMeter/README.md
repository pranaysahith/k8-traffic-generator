# JMeter PoC
Create a pod that executes a recorded script test using JMeter
# Prerequisites
## Mac OSX
### Install VirtualBox
```
    brew install virtualbox
```
### Install minikube
```
    brew install minikube
```
## Windows 10 (TBD)
# Quick Start
Running load test using JMeter against website glasswallsolutions.com
## Start minikube
```
    minikube start --driver=virtualbox
```
## Deploy artillery as a job
```
    kubectl apply -f jmeterjob.yaml
```