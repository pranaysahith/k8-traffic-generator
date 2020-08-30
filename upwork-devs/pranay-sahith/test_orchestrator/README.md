# k8s-traffic generator

## Use the shell script to deploy multiple pods of traffic generator and generate traffic for a give period of time.

* Example, to run the traffic generator with 20 users for a duration of 30 minutes run - 

    `./test.sh 20 1001 1800`
* First argument is number of users
* Second argument is test_id which can be used to uniquely identify the metrics of this run in Prometheus.
* Third argument is test duration in seconds
* Deployment/pods of each user will be deployed to a separate namespace

Prerequisites:

* deploy prometheus on the k8s cluster - `helm install prometheus stable/prometheus`
