# Helm Chart

## Prerequisites

This chart deploys an `Ingress` so the cluster should have [`ingress-nginx`](https://github.com/kubernetes/ingress-nginx) installed.

## Deploy

`helm install fd . --set apiToken="YOUR_REBUILD_API_TOKEN"`

## Configuration

Several values may be set for configuration:

| Environment Variable        | Description                            | Default                           |
| --------------------------- | -------------------------------------- | --------------------------------- |
| `apiToken`                  | Glasswall Rebuild API token            | `null`                            |
| `frontend.image.registry`   | Frontend image registry                | `docker.io` (Docker Hub)          |
| `frontend.image.repository` | Frontend image name                    | `yardenshoham/file-drop-frontend` |
| `frontend.image.tag`        | Frontend image tag                     | `latest`                          |
| `frontend.replicaCount`     | Amount of frontend instances to deploy | `latest`                          |
| `backend.image.registry`    | Backend image registry                 | `docker.io` (Docker Hub)          |
| `backend.image.repository`  | Backend image name                     | `yardenshoham/file-drop-backend`  |
| `backend.image.tag`         | Backend image tag                      | `latest`                          |
