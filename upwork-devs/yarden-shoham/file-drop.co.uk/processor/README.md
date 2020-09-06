# File Drop Processor

This container downloads a file from the URL specified in the environment variable `TARGET`, sends it to the Rebuild API (url specified by the environment variable `API_URL` with a default of `https://gzlhbtpvk2.execute-api.eu-west-1.amazonaws.com/Prod/api/rebuild/file`) using the token in the environment variable `API_TOKEN` and puts all resulting files in `/output`.
