# File Drop Backend

This container hosts a web server at port 5000. It accepts files on `/backend/files` and serves them on `/backend/static`. It saves the static files on `/usr/src/app/backend/static` in the container.

It schedules jobs that interact with File Drop using the API token from the environment variable `API_TOKEN`.
