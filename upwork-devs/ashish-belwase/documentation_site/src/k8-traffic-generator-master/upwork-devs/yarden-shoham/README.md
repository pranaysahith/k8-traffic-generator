---
slug: "/yarden-shoham"
---
# Kubernetes Traffic Generator for `glasswallsolutions.com`

This program continuously randomly chooses an interaction, executes it and waits a random interval (up to 1 second).

## Possible Interactions

- `Check PDF is downloadable and correct` - Tries to download thr PDF file from `/techonology` and verifies it's the correct file
- `Check there are at least 8 prices listed` - Checks `/pricing` lists at least 8 prices
- `Check there are exactly 3 price columns (plans) listed` - Checks `/pricing` lists exactly 3 pricing plans
- `Click a random button` - Chooses a random button at `/`, clicks on it and waits a second

## Docker Image

Quickly deploy:

`docker run -it --rm yardenshoham/k8-traffic-generator`

### Build

To build the Docker image and name it `k8-traffic-generator` run:

`docker build -t k8-traffic-generator .`

### Run

To run the aforementioned built image run:

`docker run -it --rm k8-traffic-generator`

#### Configuration

Several environment variables may be set for configuration:

| Environment Variable | Description                           | Default                  |
| -------------------- | ------------------------------------- | ------------------------ |
| `TARGET_HOST`        | Any Glasswall Solutions website clone | `glasswallsolutions.com` |

## Helm Chart

### Installing

To install the Helm chart run:

`helm install glasswall chart`

#### Configuration

Several parameters may be set for configuration:

| Parameter    | Description                           | Default                  |
| ------------ | ------------------------------------- | ------------------------ |
| `targetHost` | Any Glasswall Solutions website clone | `glasswallsolutions.com` |
