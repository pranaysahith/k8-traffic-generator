# Generate traffic and validate if files are clean

1. This will search for files in the website.
2. Download given number of files
3. Process the files through Glasswall API and validate if the files are "clean"
4. Use `RUN_FOR_MINS` environment variable to configure how much time the tests should run.
5. To run the tests only once, set the environment variable `LOOP` to `0`
6. The environment variables are configurable in docker-compose.yaml and gov-uk_job.yaml files.

## Install prerequisites (Windows)
1. Download and install Docker for Desktop from https://hub.docker.com/editions/community/docker-ce-desktop-windows/
2. Download and install kubectl from https://kubernetes.io/docs/tasks/tools/install-kubectl/#install-kubectl-on-windows

## To test in local, run

`docker-compose up --build`


## To run in kuberentes:


### Deploy Elastic to k8s by following /upwork-devs/faisal-adnan/elk/HOWTO-ELK.md

### Create a secret with elastic password in the namespace where traffic generator needs to be deployed

```
kubectl create secret generic elastic-secret --from-literal=elastic-password='update_this_with_elastic_pwd'
```

###  Deploy the job

```
kubectl deploy -f gov-uk_job.yaml
```
