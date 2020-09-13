# Windows 10 setups
## Minikube installation
Minikube installation instruction can be found at https://kubernetes.io/docs/tasks/tools/install-minikube/
We use VirtualBox Hypervisor on all the systems including Windows 10
### Starting Minikube
You can start Minikube from an elevated command prompt or Windows PowerShell.
Use the following command: 
```
minikube start --driver=virtualbox --cpus=3 --memory=8192
```
## kubectl installation
Download kubectl from https://storage.googleapis.com/kubernetes-release/release/v1.19.0/bin/windows/amd64/kubectl.exe. 
To make it accessible from the command line, put kubctl.exe into 
```
C:\Windows\System32
``` 
folder. This is where most Windows utilities are located.
### The Docker Environment
Minikube has its own docker environment. One may need to access to clean cached container images. Developers may use it for building the images to be utilized by the local Minikube setup. 
To enable the minicube docker environment to run the command in elevated Windows PowerShell:
```
PS C:\WINDOWS\system32> minikube docker-env
```
The result will look similar to the following:
```
$Env:DOCKER_TLS_VERIFY = "1"
$Env:DOCKER_HOST = "tcp://192.168.99.117:2376"
$Env:DOCKER_CERT_PATH = "C:\Users\admin\.minikube\certs"
$Env:MINIKUBE_ACTIVE_DOCKERD = "minikube"
# To point your shell to minikube's docker-daemon, run:
# & minikube -p minikube docker-env | Invoke-Expression
```
Run each line starting with `$Env:`. This will be needed only once. Then switch to Minikube docker environment with 
```
& minikube -p minikube docker-env | Invoke-Expression
```
### Noticed flaws
In some cases, Minikube fails to download container images from the Docker hub. The downloads start but then get frozen. This usually causes failure of deployments in minikube. The easiest way found to get around this is to restart minikube, switch on minikube docker environment, and pull the corresponding image there. 
## ELK
The most trivial way to deploy ELK in local Minikube setup is with the following manifest (elk.yaml):
```
piVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch
spec:
  version: 7.8.0
  nodeSets:
  - name: default
    count: 1
    config:
      node.master: true
      node.data: true
      node.ingest: true
      node.store.allow_mmap: false
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 10Gi       
---
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana
spec:
  version: 7.8.0
  count: 1
  elasticsearchRef:
    name: elasticsearch

```
The manifest utilizes version 7.8.0 for both Elasticsearch and Kibana. More recent versions may be utilized. 

Running
```
kubectl apply -f elk.yaml
```
will deploy password protected Elasticsearch and Kibana. 
Other pods on the node can access those with the corresponding URLs:
```
https://kibana-kb-http:5601
https://elasticsearch-es-http:9200
```
The passcode for user 'elastic' may be obtained with the following command
```
kubectl get secret elasticsearch-es-elastic-user -o go-template="{{.data.elastic | base64decode}}"
```
In some cases, it may be helpful to switch password protection for Elasticsearch off. For instance, a POD with a pre-configured filebeat setup may need such access to send logs to the ELK. This may be achieved by adding the following to the 
```
    config:
      xpack.security.authc:
        anonymous:
          username: anonymous
          roles: superuser
          authz_exception: false
```
### ELK with Filebeat
For ELK deployment with a Filebeat POD see step by step instructions at:

https://github.com/filetrust/k8-traffic-generator/blob/master/upwork-devs/faisal-adnan/elk/HOWTO-ELK.md

### ELK with Pakcetbeat
For ELK deployment with a Packetbeat POD see step by step instructions at:

https://github.com/filetrust/k8-traffic-generator/tree/master/upwork-devs/harut-gigoryan/packetbeat-poc  

## Minio
The step by step guide for deploying Minio 

https://github.com/filetrust/k8-traffic-generator/tree/master/upwork-devs/susanta-gautam/minio-traffic-generator/minio

utilizing Nodeport, has been tested on Windows 10.

## JMeter
To deploy a JMeter POD firstly build a docker image from: 
https://github.com/filetrust/k8-traffic-generator/tree/master/upwork-devs/faisal-adnan/JMeter
utilizing minikube docker environment in Windows PowerShell (as explained above): 
```
PS C:\WINDOWS\system32> & minikube -p minikube docker-env | Invoke-Expression
PS C:\WINDOWS\system32> cd C:\Projects\Glasswall\k8-traffic-generator\upwork-devs\faisal-adnan\JMeter
PS C:\Projects\Glasswall\k8-traffic-generator\upwork-devs\faisal-adnan\JMeter> docker build -t test/jmeter .
```
Then deploy the POD:
```
PS kubectl apply -f test/jmeter
```

## Artillery

