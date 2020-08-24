# k8-traffic-generator

## Docker Image

Quickly deploy:

`docker run -it --rm yardenshoham/k8-traffic-generator`

### Configuration

Several environment variables may be set for configuration:

| Environment Variable | Description                           | Default                  |
| -------------------- | ------------------------------------- | ------------------------ |
| `TARGET_HOST`        | Any Glasswall Solutions website clone | `glasswallsolutions.com` |

If you are working on this project via Upwork, see also our [Upwork Rules of Engagement](https://github.com/filetrust/Open-Source/blob/master/upwork/rules-of-engagement.md)

### Project brief

**Objective**: Create a Kubernetes (K8) native application that is able to generate large amounts of web traffic (namely file downloads)

- In order to effectively test the [Glasswall ICAP project](https://github.com/filetrust/program-icap) we need a test framework that is able to simulate user traffic like:
  - Open pages
  - Follow links
  - Upload files
  - Download files
- Key concept is to use each K8 pod as an 'user', which depending on some configurable values, will perform a number of pre-determined or random actions
- Key objective is to be able to use this K8 solution to scale up and down the traffic (which should simply be a case of adding or removing pods from the cluster)
  - key milestone is to be able to find the limitations of a particular ICAP deployment
- CI and CD pipeline are a key requirement (with the entire test scenario being able to be executed from scratch)
- Target execution environments for the k8 environment:
  - locally (using Docker Desktop)
  - EC2 or Azure VM (with K8 installed)
  - Managed EKS (AWS or Azure)
- implement logging solutions to visualize what is going on inside the K8 environnement (with a special focus on the individual pods actions and the server's responses)
