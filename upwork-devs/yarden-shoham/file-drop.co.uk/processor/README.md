# File Drop Processor

This container grabs all files in `/input`, sends them to the Rebuild API use the token in the environment variable `API_TOKEN` and puts all resulting files in `/output`.
