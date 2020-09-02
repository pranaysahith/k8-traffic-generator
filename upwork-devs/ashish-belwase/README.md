# Kubernetes Traffic Generator

## Docker Image

### Build

To build the Docker image and name it `k8-traffic-generator` run:

`docker build -t k8-traffic-generator .`

### Run

To run the aforementioned built image run:

`docker run -it --rm k8-traffic-generator`

#### Configuration

There are two modes: `traffic` or `testing`. The default mode is `traffic` which does load testing. The `testing` mode simply runs unit tests. To set the mode, set the environment variable `MODE`.

For the `traffic` mode, several environment variables may be set for configuration:

| Environment Variable | Description                                               | Default                           |
| -------------------- | --------------------------------------------------------- | --------------------------------- |
| `URL`                | URL of site to load traffic                               | `https://glasswallsolutions.com/` |
| `ACTION`             | Action to perform, see [Valid Actions](#possible-actions) | Empty (Perform random action)     |

##### Valid Actions

Any site: [`open`, `follow`, `download`, `upload`]

`glasswallsolutions.com`: [`products`, `pricing`, `company`, `random_click`]

## Elastic ELK Setup

```
Refer:    /upwork-devs/faisal-adnan/elk/HOWTO-ELK.md
```
