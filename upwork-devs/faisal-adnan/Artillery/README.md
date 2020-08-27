# Artillery PoC
Create a pod that executes test using Artillery
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
Running testing with the following phases and scenario:
## Phase
```mermaid
graph LR
    Warm --> Ramp --> Peak
```
- Warming up 
    - Arrival rate of 2 for 60 seconds
- Ramping up
    - Arrival rate of 2 to 5 for 300 seconds
- Peak
    - Arrival rate of 5 for 600 seconds
## Scenario
Each virtual user will do the following:
- Open https://glasswallsolutions.com/technology
- Open https://glasswallsolutions.com/products
- Open https://glasswallsolutions.com/pricing
- Open https://glasswallsolutions.com/resources
- Open https://glasswallsolutions.com/company
## Start minikube
```
    minikube start --driver=virtualbox
```
## Deploy artillery as a job
```
    kubectl apply -f artillery-job.yaml
```
