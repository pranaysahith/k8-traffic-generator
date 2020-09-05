# File Drop Backend

This container hosts a web server at port 5000. It accepts files on `/backend/files` and serves them on `/backend/static`. It saves the static files on `/usr/src/app/backend/static` in the container.

It schedules jobs (processor containers specified by the environment variable `PROCESSOR_IMAGE` with a default of `yardenshoham/file-drop-processor`) that interact with File Drop (with the URL from the environment variable `API_URL` that defaults to `https://gzlhbtpvk2.execute-api.eu-west-1.amazonaws.com/Prod/api/rebuild/file`) using the API token from the environment variable `API_TOKEN`.
