## Minio deployment

While replicating the minio demo in your test environment, please go through the following steps.


1. Deploy the minio deployment files.

    `kubectl apply -f minio/minio-deployment.yaml`

2. Deploy the minio service files.

    `kubectl apply -f minio/service.yaml`

3. Validate your minio deployment and service in there respective environment.

    `kubectl get all`
 
6. Now let's go for the local setup (Minikube/Docker Desktop).

    `kubectl apply -f minio/nodeport.yaml`

7. Get the Nodeport exposed by the service. (Please Note that the NodePort of yours can differ with mine.)

    `kubectl get svc`

    You should get the output like below. In this case the Nodeport exposed is 31910.

    `input-queue-nodeport   NodePort    10.100.73.127   <none>        9000:31910/TCP   45m`

    `output-queue-nodeport   NodePort    10.100.195.45    <none>        9000:31322/TCP   50m`

8. Get your minikube ip. As for the docker desktop you should be able to get it from the ipconfig.

    `minikube ip`

9. Now you can access the input-queue in your browser with http://<minikube_ip>:31910 && output-queue with http://<minikube_ip>:31322


