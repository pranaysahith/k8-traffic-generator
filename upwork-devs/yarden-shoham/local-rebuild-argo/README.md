# Local Rebuild Using Argo

This workflow gets an S3 storage endpoint as an input, spins up a pod to run each file in the S3 bucket through the Rebuild engine and sends the reports to Elasticsearch.

## Quick Start

Install argo with artifacts.

```bash
kubectl create ns argo
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/quick-start-postgres.yaml
kubectl -n argo port-forward deployment/argo-server 2746:2746
```

Run the workflow.

```bash
argo submit workflow.yaml -n argo
```

or

```bash
kubectl create -f workflow.yaml -n argo
```

## Configuration

Several parameters may be specified for configuration:

| Parameter            | Description         | Default                                    |
| -------------------- | ------------------- | ------------------------------------------ |
| `imageRegistry`      | Image registry      | `docker.io`                                |
| `endpoint`           | S3 endpoint         | `play.min.io`                              |
| `accessKey`          | S3 access key       | `Q3AM3UQ867SPQQA43P2F`                     |
| `secretKey`          | S3 secret key       | `zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG` |
| `bucketName`         | S3 bucket name      | `yarden-test`                              |
| `elasticsearchHost`  | Elasticsearch host  | `host.docker.internal`                     |
| `elasticsearchPort`  | Elasticsearch port  | `9200`                                     |
| `elasticsearchIndex` | Elasticsearch index | `reports`                                  |

To apply configuration, create a yaml file:

`params.yaml`

```yaml
endpoint: YOUR_S3_ENDPOINT
accessKey: YOUR_S3_ACCESS_KEY
secretKey: YOUR_S3_SECRET_KEY
bucketName: YOUR_S3_BUCKET_NAME
elasticsearchHost: YOUR_ELASTICSEARCH_HOST
```

Run the workflow while supplying the file.

```bash
argo submit workflow.yaml --parameter-file params.yaml -n argo
```
