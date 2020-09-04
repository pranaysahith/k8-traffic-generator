# File Drop Processor

This container downloads a file from the URL specified in the environment variable `TARGET`, sends it to the Rebuild API using the token in the environment variable `API_TOKEN` and puts all resulting files in `/output`.
