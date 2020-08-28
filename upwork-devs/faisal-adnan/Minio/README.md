## Install minikube
```
    brew install minikube
```
## Start minikube
```
    minikube start --driver=virtualbox
```
## Deploy Minio 
```
    git clone https://github.com/minio/operator.git
    cd operator
    kubectl apply -k github.com/minio/operator
    kubectl apply -f https://raw.githubusercontent.com/minio/operator/master/examples/tenant.yaml
    kubectl port-forward service/minio 9000:9000
```
### Open Minio UI on http://localhost:9000
See screenshot ![minio](minio.png)
### Login to UI
- User: minio
- Password: minio123
## Upload files
### Using S3 API from Python
```sequenceDiagram
    TrafficGenerator->>Minio: boto.s3_client.upload_file(File)
    Minio-->>OK
```
## Download files
### Using S3 API from Python
```sequenceDiagram
    TrafficGenerator->>Minio: boto.s3_client.download_fileobj(File)
    Minio-->>File
```