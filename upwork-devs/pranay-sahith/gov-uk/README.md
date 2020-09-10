# Generate traffic and validate if files are clean

1. This will search for files in the website.
2. Download given number of files
3. Process the files through Glasswall API and validate if the files are "clean"

## To test in local, run

`docker-compose up --build`


## To run in kuberentes, deploy the job:

`kubectl deploy -f gov-uk_job.yaml`

