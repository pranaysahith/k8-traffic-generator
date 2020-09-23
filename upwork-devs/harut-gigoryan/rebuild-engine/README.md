# Rebuild engine as the target system
This implements the design at:

https://github.com/k8-proxy/k8-traffic-generator/blob/master/docs/rebuild-engine-as-a-target.md

Minio instances are utilized for file input and output queues
Logs are sent to ELK by filebeat instances running on File Processing PODs 
The logs are in JSON format

## Node Setup

### ELK
To setup ELK on the node run
```
    kubectl apply -f all-in-one.yaml
    kubectl apply -f elk.yaml
```
Get the credentials
Username: elastic
Password: see command below
```
    kubectl get secret elasticsearch-es-elastic-user -o go-template="{{.data.elastic | base64decode}}"
```
Forward Kibana service port to be accessible on the localhost. 
```
    kubectl port-forward service/kibana-kb-http 5601
```
Open Kibana on https://localhost:5601


### Minio
To setup Minio instances on the node run 
```
    kubectl apply -f minio.yaml
```
Find out the NodePort ports for accessing the Minio instances
```
   kubectl get svc
   NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORTTCP         25h
   .....
   input-queue-nodeport         NodePort    10.98.121.211   <none>        9000:30747/TCP   25h
   .....
   output-queue-nodeport        NodePort    10.98.36.7      <none>        9000:31555/TCP   25h
```
Find out the IP
```
    minikube IP
    192.168.99.120
```
With the IP and port values obtained as above access
- the input queue at http://192.168.99.120:30747/minio/login
- the output queues at http://192.168.99.120:31555/minio/login

Access Key: test
Secret Key: test@123


### Inspector
You must have Python installed on your system
Also, install the following packages
```
    pip install requests
    pip install python-json-logger
    pip install kubernetes
```
Start the Inspector process as following
```
    python .\inspector\inspector.py
```
Inspector stores the logs in `.\inspector\application.log`

