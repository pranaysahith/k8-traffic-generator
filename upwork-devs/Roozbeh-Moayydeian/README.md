## Diagram:

<img src="./img/diagram.png" alt="Diagram" width="700"/>

_____

## Monitoring Overview:

<div align="left">
<img src="./img/jaeger.png" alt="Diagram" width="100"/>
<img src="./img/kiali.png" alt="Diagram" width="100"/>
<img src="./img/rancher.png" alt="Diagram" width="100"/>
<img src="./img/grafana1.png" alt="Diagram" width="100"/>
<img src="./img/grafana2.png" alt="Diagram" width="100"/>
<img src="./img/grafana3.png" alt="Diagram" width="100"/>
</div>

_______

## Installation:

### * Replace these variables in all files:
```
{HOST_IP} with your host local ip address
{MINIKUBE_IP} with your minikube IP (Run: minikube ip)
```

#### - Pull git repository:
```
git clone {REPO_URL}
cd {REPO_DIRECTORY}
```
#### - Create local docker registery on your host:
```
docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

#### - Start minikube with 16384 MB of memory and 4 CPUs. This example uses Kubernetes version 1.17.5. You can change the version to any Kubernetes version supported by Istio by altering the --kubernetes-version value:

```
minikube start --driver=kvm2 --memory=16384 --cpus=4 --insecure-registry="{HOST_IP}:5000"
```
#### - Start Rancher pannel for easy maintenance and monitoring:
```

docker run -d --restart=unless-stopped \
  -p 8080:80 -p 4433:443 \
  rancher/rancher:latest
```

#### - Install basic modules in order:

```
kubectl apply -f Installation/setup-istio.yaml
kubectl apply -f Installation/setup-prometheus.yaml
kubectl apply -f Installation/setup-jaeger.yaml
kubectl apply -f Installation/setup-grafana.yaml
kubectl apply -f Installation/setup-kiali.yaml
kubectl apply -f Installation/basic-dep.yaml
```

#### - Label default namespace for auto inject istio:
```
kubectl label namespace default istio-injection=enabled
```
#### - Deploy nginx deployment as target service:
```
kubectl apply -f nginx-dep.yaml
```

## Note: change istio-ingressgateway service to NodePort

### - Get Istio Ingressgateway NodePort:
```
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')

export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')

export TCP_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="tcp")].nodePort}')

```

### - Add client host if you don't user dns or FQDN

```
echo "{MINIKUBE_IP} gw-nginx-service.local kiali-service.local grafana-service.local jaeger-service.local" > /etc/hosts
```

### - You may access to this urls:

```
https://{HOST_IP}:4433
http://gw-nginx-service.local:$INGRESS_PORT/
http://kiali-service.local:$INGRESS_PORT/
http://grafana-service.local:$INGRESS_PORT/
http://jaeger-service.local:$INGRESS_PORT/
```

### - Build LoadGenerator:

```
cd LoadGenerator

docker build -t {HOST_IP}:5000/load-generator:latest .
```

### - Push image to local repo:

```
docker push {HOST_IP}:5000/load-generator:0.0.3
```

### - Test scenario and target urls
```
1. Open load-generator-dep.yaml
2. Customize REQUEST_TYPES environment variable in Configmap.

You can set the list of APIs you want to test in order.
Fully customizable (GET, POST, PUT, DELETE, Upload Files using form-data, custom headers and authentication, ...)

Full Doc:
https://nodejs.org/api/http.html

ex: 

[
        {
            "host": "nginx-service",
            "port": 80,
            "path": "/",
            "protocol": "http:",
            "method": "GET",
            "headers": {
                "Content-Type": "application/json"
            }
        },
        {
            "host": "nginx-service",
            "port": 80,
            "path": "/fake-path",
            "protocol": "http:",
            "method": "GET",
            "headers": {
                "Content-Type": "application/json"
            }
        }
    ]
```

### - Apply LoadGenerator deployment (variable replace needed):

```
kubectl apply -f load-generator-dep.yaml
```

### Results:
#### Stats with 3 LoadGenerator pods:

<div align="left">
<img src="./img/3replica/1-rancher.png" alt="1-rancher" width="100"/>
<img src="./img/3replica/2-lg-deployment.png" alt="2-lg-deployment" width="100"/>
<img src="./img/3replica/3-nginx-pod.png" alt="3-nginx-pod" width="100"/>
<img src="./img/3replica/4-kiali.png" alt="4-kiali" width="100"/>
<img src="./img/3replica/5-istio.png" alt="5-istio" width="100"/>
</div>

____________________________

#### Stats with 2 LoadGenerator pods:

<div align="left">
<img src="./img/2replica/1-rancher.png" alt="1-rancher" width="100"/>
<img src="./img/2replica/2-lg-deployment.png" alt="2-lg-deployment" width="100"/>
<img src="./img/2replica/3-nginx-pod.png" alt="3-nginx-pod" width="100"/>
<img src="./img/2replica/4-kiali.png" alt="4-kiali" width="100"/>
<img src="./img/2replica/5-istio.png" alt="5-istio" width="100"/>
</div>

____________________________

#### Stats with 1 LoadGenerator pod:

<div align="left">
<img src="./img/1replica/1-rancher.png" alt="1-rancher" width="100"/>
<img src="./img/1replica/2-lg-deployment.png" alt="2-lg-deployment" width="100"/>
<img src="./img/1replica/3-nginx-pod.png" alt="3-nginx-pod" width="100"/>
<img src="./img/1replica/4-kiali.png" alt="4-kiali" width="100"/>
<img src="./img/1replica/5-istio.png" alt="5-istio" width="100"/>
</div>
