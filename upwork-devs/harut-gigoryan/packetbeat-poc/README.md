# Packetbeat POC 
Start minikube
```
    minikube start --driver=virtualbox --cpus=3 --memory=8192
```
Create ECK operator
```
    kubectl apply -f all-in-one.yaml
```
Deploy ELK along with packetbeat deamon set. This may take 5+ minutes.
```
    kubectl apply -f packetbeat.yaml
```
Get the credentials
Username: elastic
Password: see command below
```
    kubectl get secret elasticsearch-es-elastic-user -o go-template="{{.data.elastic | base64decode}}"
```
Forward Kibana service port to be accessible on the locahost. 
```
    kubectl port-forward service/kibana-kb-http 5601
```
Open Kibana on https://localhost:5601
If necessary, add packetbeat-* to the Index Pattern 
Continue with packetbeat dashboards in Kibana