# Generate traffic and validate if files are clean

1. This will search for files in the website.
2. Download given number of files
3. Process the files through Glasswall API and validate if the files are "clean"
4. Use `RUN_FOR_MINS` environment variable to configure how much time the tests should run.
5. To run the tests only once, set the environment variable `LOOP` to `0`
6. The environment variables are configurable in docker-compose.yaml and gov-uk_job.yaml files.

## To test in local, run

`docker-compose up --build`


## To run in kuberentes, deploy the job:

`kubectl deploy -f gov-uk_job.yaml`

