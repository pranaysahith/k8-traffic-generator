## Kube-state-metrics and Metricbeats for collecting Cluster information

Here we are using kubestate metrics and metricbeats to collect the kubernetes metrics that will be displayed in the kibana dashboard. Here various component would be used to collect the various data. Following are the component that will be used.

1. kube-state-metrics:
    KubeStateMetrics is the application that will be deployed in the kubesystem namespace. It will be responsible for collecting various information from the kubernetes apiserver. These metrics will then be collected by the metricbeat.
2. Metricbeat(Deployment):
    We will be deploying one replica of the metricbeat that will be solely responsible for collecting the information from the kubernetes component such as scheduler, kube-controller, apiserver metrics, metrics from kube-state-metric. I have configured it to be deployed in master node as it needs to connect to the kube-scheduler and kube-controller which in default run on master node and bind the localhost port(127.0.0.1). If we want this comonennt to run on the other node, there are two options. That is either we bind the scheduler and controller on host (0.0.0.0) or we give up on the metrics of these two component. In case you want to giveup on the component please comment the following section from the configmap of file [metricbeat-deployment-with-dashboard.yaml](metricbeats/metricbeat-deployment-with-dashboard.yaml) or [metricbeat-deployment.yaml](metricbeats/metricbeat-deployment.yaml) based on your preference. The section to comment is:
    ```YAML
    - module: kubernetes
      enabled: true
      ssl.certificate_authorities:
        - /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      ssl.verification_mode: none
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      metricsets:
        - controllermanager
      hosts: ["https://localhost:10257"]
      peroid: 20s
    - module: kubernetes
      enabled: true
      ssl.certificate_authorities:
        - /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
      ssl.verification_mode: none
      metricsets:
        - scheduler
      hosts: ["https://localhost:10259"]
      peroid: 30s
    ```
    Also you will need to remove the node affinity and toleration in the pod spec section in same file.
3. Metricbeat(daemonset):
    we will ne using the metricbeat daemonset to collect the metrics of the host system. The daemonset will be collecting the the data of the system like disk usage, cpu usage, cpu load, network stats etc. It will also collect the information from kubelet that are pertaining to node, volumes, pod, system and kube-proxy. 
4. ElasticSearch:
    We will be sending the data to elastic search from all the metricbeat instances. You can use the another project for configuring the ELK stack and docs are avaliable in [documentation](https://github.com/filetrust/k8-traffic-generator/tree/master/docs). Keep in mind you will need to provide the username and password for the elasticsearch and you will need to provide the valid elasticsearch url(in k8s case service name).
    ```YAML
    output.elasticsearch:
      hosts: ['${ELASTICSEARCH_HOST:elasticsearch-master}:${ELASTICSEARCH_PORT:9200}']
      # username: ${ELASTICSEARCH_USERNAME}
      # password: ${ELASTICSEARCH_PASSWORD}
    ```
5. Kibana:
    Kibana dashboard will be used to visualize the metrics of the cluster. There are two deployment manifest for the deployment. IF you use the one with the setup dashboard you will need to add the data about the kibana in the configmap. The code section will be:
    ```YAML
    setup.dashboards.enabled: true
    setup.kibana:
      host: "kibana-kibana:5601"
      kibana.protocol: "http"
      # username: givemeusername
      # password: givemepassword
    ```

## Configuration Part

Here while configuring elasticsearch and kibana, i am using elastic helm repo. In production environment we will have ELK stack already configured to which we will be feeding the data.

```bash
    # Create elk namespace
    $ kubectl create ns elk
    # Install elasticsearch
    $ helm install elasticsearch elastic/elasticsearch --values helm-elasticsearch/values.yaml -n elk
    # Install Kibana
    $ helm install kibana elastic/kibana -n elk
    # Here i am using istio ingressgateway for ingress. If you are using minikube environment, use nodeport for accessing the kibana.
    $ kubectl apply -f kibana-ingress/
```

Now let's deploy the kube-state-metric in the cluster.
```BASH
    $ kubectl apply -f kube-state-metrics/
```
Deploy the metrics beats to the cluster.
```bash
    # Apply the ClusterRole and Serviceaccount for metricbeat.
    $ kubectl apply -f metricbeats/clusterRole.yaml
    # Apply the daemonset. This manifest will not deploy the daemonset to the master node on its own. if you want to have one pod in master node please add the tolaration in the pod spec section.
    $ kubectl apply -f metricbeats/metricsbeats-daemonset.yaml
    # Apply metricbeats deployment file of your choise. You can deploy only one among two (metricbeat-deployment.yaml or metricbeat-deployment-with-dashboard.yaml)
    $ kubectl apply -f metricbeats/metricbeat-deployment-with-dashboard.yaml 
```

Now you can check the pods status by running the following command.
```
    $ kubectl get pods -n elk
```

It will take some amount of time for all of these services to be configured. After all the pods are functional, you can visit the kibana dashboard to check the metrics.