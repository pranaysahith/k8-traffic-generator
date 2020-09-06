# Helm Chart

## Prerequisites

This chart deploys an `Ingress` so the cluster should have [`ingress-nginx`](https://github.com/kubernetes/ingress-nginx) installed.

## Deploy

```bash
.../file-drop.co.uk/chart$ helm install fd . --set api.token="YOUR_REBUILD_API_TOKEN"
```

### Configuration

Several values may be set for configuration:

| Parameter                    | Description                            | Default                                                                        |
| ---------------------------- | -------------------------------------- | ------------------------------------------------------------------------------ |
| `api.url`                    | Glasswall Rebuild API URL              | `https://gzlhbtpvk2.execute-api.eu-west-1.amazonaws.com/Prod/api/rebuild/file` |
| `api.token`                  | Glasswall Rebuild API token            | `null`                                                                         |
| `frontend.image.registry`    | Frontend image registry                | `docker.io` (Docker Hub)                                                       |
| `frontend.image.repository`  | Frontend image name                    | `yardenshoham/file-drop-frontend`                                              |
| `frontend.image.tag`         | Frontend image tag                     | `latest`                                                                       |
| `frontend.replicaCount`      | Amount of frontend instances to deploy | `1`                                                                            |
| `backend.image.registry`     | Backend image registry                 | `docker.io` (Docker Hub)                                                       |
| `backend.image.repository`   | Backend image name                     | `yardenshoham/file-drop-backend`                                               |
| `backend.image.tag`          | Backend image tag                      | `latest`                                                                       |
| `processor.image.registry`   | Processor image registry               | `docker.io` (Docker Hub)                                                       |
| `processor.image.repository` | Processor image name                   | `yardenshoham/file-drop-processor`                                             |
| `processor.image.tag`        | Processor image tag                    | `latest`                                                                       |
