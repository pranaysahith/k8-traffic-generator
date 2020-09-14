# Generate traffic on Next Cloud website

## Install next cloud

```
kubectl create ns nextcloud
helm upgrade --install nextcloud stable/nextcloud \
  --namespace nextcloud \
  --values nextcloud.values.yml
```

## Generate traffic using docker-compose. Next cloud is exposed on port 9090

```
docker-compose up --build
```

## Generate traffic using k8s

```
kubectl apply -f traffic_generator.yaml
```

### The pod sends metrics to prometheus and logs to ELK [TBD]


```graphviz
digraph {
    
    rankdir=LR
    
    n1 [ shape=box, label="shell script"]
    n2 [ shape=box, label="TG pods 1-N"]
    n3 [ shape=box, label="Next Cloud"]
    n4 [ shape=box, label="Prometheus"]
    n5 [ shape=box, label="ELK"]
    
    n1 -> n2
    n2 -> n3 [label="download/upload files"]
    n2 -> n4 [label="send metrics"]
    n2 -> n5 [label="send logs"]
    
}
```
