## Documentation about the minio demo

While replicating the minio demo in your test environment, please go through the following steps.

1. Make sure you already have kubectl configured for your cluster.
2. Create the namespaces minio-one, minio-two, minio-test for minio deployment one and two and traffc generator code respectively.

    `kubectl create ns minio-one`

    `kubectl create ns minio-two`
    
    `kubectl create ns minio-test`

3. Deploy the minio deployment files.

    `kubectl apply -f minio/minio-deployment.yaml`

4. Deploy the minio service files.

    `kubectl apply -f minio/service.yaml`

5. Validate your minio deployment and service in there respective environment.

    `kubectl get all -n minio-one`

    `kubectl get all -n minio-two`

6. Now there are two ways to expose the minio to the outer world. In the demo i have used istio ingressgateway. You can use the choise of your own. You can choose to have the ingress controller of your choise or use the NodePort service to expose the application. Let's first go through the ingress.

    `kubectl apply -f ingress.yaml`

7. Verify the ingress resource created.

    `kubectl get ingress --all-namespaces`

    Note: Please look for the one with the namespace minio-one and minio-two.

8. As the ingress has been configured with the non existent hostname (minio-one.example.com && minio-two.example.com) you will need to add the host entry of your pc. For mac and linux user please add the entry in "/etc/hosts" and for windows user "c:\Windows\System32\Drivers\etc\hosts". The ip will be your loadbalancer IP.

9. Now let's go for the local setup (Minikube/Docker Desktop).

    `kubectl apply -f minio/nodeport.yaml`

10. Get the Nodeport exposed by the service. (Please Note that the NodePort of yours can differ with mine.)

    `kubectl get svc -n minio-one`

    You should get the output like below. In this case the Nodeport exposed is 31910.

    `minio-one-nodeport   NodePort    10.100.73.127   <none>        9000:31910/TCP   45m`

    `kubectl get svc -n minio-two`

    You should get the output. In this case the nodeport exposed is 31322

    `minio-two-nodeport   NodePort    10.100.195.45    <none>        9000:31322/TCP   50m`

11. Get your minikube ip. As for the docker desktop you should be able to get it from the ipconfig.

    `minikube ip`

13. Now you can access the minio-one in your browser with http://<minikube_ip>:31910 && minio-two with http://<minikube_ip>:31322

14. If you have istio deployed in your cluster, you can follow the following steps.

    `kubectl label ns minio-one istio-injection=enabled`

    `kubectl label ns minio-two istio-injection=enabled`

    `kubectl label ns minio-test istio-injection=enabled`

    `kubectl apply -f gateway.yaml`

    `kubectl apply -f virtualservice.yaml`

    Using this, you can access the service same as you are using the nginx or traefik ingress controller by using domain name.

14. Now you can deploy the traffic generator.

    `kubectl apply -f miniotraffic-deployment.yaml`

