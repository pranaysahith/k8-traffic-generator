# Minio traffic generator with ELK

1. create namespace to deploy minio - `kubectl create ns minio`
2. deploy minio pods and services to k8s - `kubectl -n minio apply -f minio_service.yaml`
3. build docker 
4. deploy traffic generator
5. watch elk logs