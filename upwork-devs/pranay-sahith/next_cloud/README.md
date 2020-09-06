# Generate traffic on Next Cloud website

## Install next cloud

```
kubectl create ns nextcloud
helm upgrade --install nextcloud stable/nextcloud \
  --namespace nextcloud \
  --values nextcloud.values.yml
```

## Generate traffic using docker-compose

```
docker-compose up --build
```

## Generate traffic using k8s

```
kubectl apply -f traffic_generator.yaml
```

