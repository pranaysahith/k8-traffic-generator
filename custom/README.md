## Docker Image

Quickly deploy:

`docker run -it --rm yardenshoham/k8-traffic-generator`

### Build

`docker build -t k8-traffic-generator .`

### Run

`docker run -it --rm k8-traffic-generator`

#### Configuration

Several environment variables may be set for configuration:

| Environment Variable | Description                           | Default                  |
| -------------------- | ------------------------------------- | ------------------------ |
| `TARGET_HOST`        | Any Glasswall Solutions website clone | `glasswallsolutions.com` |
