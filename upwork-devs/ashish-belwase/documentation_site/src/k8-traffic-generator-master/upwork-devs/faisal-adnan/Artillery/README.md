---
slug: "/faisal-adnan/artillery"
---
# Artillery PoC
Create a pod that executes test using Artillery
# Quick Start 
This project execute a test scenario by running it in 1 to N pods.
The pod generates the following data:
1. The test log is shipped to ELK
2. The test report is uploaded to Minio.
3. The http tracing is sent to Zipkin or Jaeger.

See the diagram below:

```ditaa {cmd=true args=["-E"]}
+----+-----+            +-------------------------------------------+
| Scenario |            | K8S                    +-----------+      |
| File     |            |                        |           |      |   
| {d}      |            |         +------------->|  Jaeger   |      |  
+----+-----+            |         |              |   (WIP)   |      |
     |                  |         |              +-----------+      |
     |                  |         |                                 |
     |        Deploy    |         |                                 |
+----+-----+  to 1 - N  |   +-----+-----+        +-----------+      |
|          |  pods      |   |   Istio   |        |           |      |
| Shell    +----------->|   | side car  | report |           |      |
| Script   |            |   +-----------+------->|   Minio   |      |
|          |            |   | Artillery |        |           |      |
|          |            |   |    Pod    |        |           |      |
+----+-----+            |   +-+----+----+        +-----------+      |
                        |     ^    |                                |
                        |     |    |             +-----------+      |
                        |     |    |             |           |      |
                        |     |    |   logging   |           |      |
                        |     |    +------------>|    ELK    |      |
                        |     |                  |           |      |
                        |   +-+---------+        |           |      |
                        |   |   Vault   |        +-----------+      |
                        |   |   for     |                           |
                        |   |   Scenario|                           |
                        |   |   file    |                           |
                        |   |   and     |                           |
                        |   |   secrets |                           |
                        |   +-----------+                           |
                        +-------------------------------------------+

```
## Start minikube
```
    minikube start --feature-gates=TTLAfterFinished=true --driver=virtualbox
```
## Deploy artillery as a job
```
    sh run.sh <artillery_config_file> <number_of_pods>
```
