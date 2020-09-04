## Add Minio Operator
```
    git clone https://github.com/minio/operator.git
    cd operator
    kubectl apply -k github.com/minio/operator
```
## Deploy Standalone Minio Tenant
```
    kubectl apply -f tenant-SA.yaml
```
## Open Minio UI on https://localhost:9000
```
    kubectl port-forward service/minio 9000:9000
```
See screenshot ![minio](minio.png)
### Login to UI
- User: minio
- Password: minio123
## Upload files
### Using S3 API from Python
```sequence {theme="simple"}
TrafficGenerator->Minio: boto.s3_client.upload_file
Minio-->TrafficGenerator:OK
```
## Download files
### Using S3 API from Python
```sequence {theme="simple"}
    TrafficGenerator->Minio: boto.s3_client.download_fileobj(File)
    Minio-->TrafficGenerator:File
```