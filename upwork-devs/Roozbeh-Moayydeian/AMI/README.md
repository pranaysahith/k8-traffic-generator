# How to create AMI (Amazon Machine Image) for k8s

<img src="https://d39w7f4ix9f5s9.cloudfront.net/dims4/default/f41a71b/2147483647/strip/true/crop/1200x542+0+44/resize/1440x650!/quality/90/?url=http%3A%2F%2Famazon-blogs-brightspot.s3.amazonaws.com%2F40%2Fb0%2F16d665224675bf7ecf4431d1e9ca%2Faws-logo-smile-1200x630.png" alt="aws" width="500"/>

_____

An Amazon Machine Image (AMI) provides the information required to launch an instance. You must specify an AMI when you launch an instance. You can launch multiple instances from a single AMI when you need multiple instances with the same configuration. You can use different AMIs to launch instances when you need instances with different configurations.

_____

- Open createAMI.sh
- Cutomize default values and run ```./createAMI.sh``` or send your custom values inline:
```
./createAMI.sh roozbeh ami-0dba2cb6798deb6d8 testing-kubernetes AMItest t2.micro gw-ami-test
```

- type ./createAMI.sh --help for more information

```
Please set your parameters as metioned below
./createAMI.sh KEY_NAME BASE_IMAGEID SECURITY_GROUP INSTANCE_NAME INSTANCE_TYPE AMI_NAME
```

- It may take a few minutes for the AMI to be created. After it is created, it will appear in the AMIs view in AWS Explorer. To display this view, double-click the Amazon EC2 | AMIs node in AWS Explorer. To see your AMIs, from the Viewing drop-down list, choose Owned By Me. You may need to choose Refresh to see your AMI. When the AMI first appears, it may be in a pending state, but after a few moments, it transitions to an available state.

Now your custom AMI for bare-metal k8s is ready!
_____
_____
# * How it works?
## 1. First Create your EC2 Instances

Full doc on: https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html

You just need to configure ```run-instances-skeleton.json``` file.

You can see all available options in ```run-instances-skeleton-example.json``` file.

note:
  - It's already configed for minimal instance for docker installation.
  - Uppercase options like 'BASE_IMAGEID' or 'KEY_NAME' automatically replaced from createAMI.sh. just add cutomaize options if needed.
  - add your instance preparation script as UserData ex: see UserData.sh (full doc: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)

## 2. Now it's time to make an AMI image for future use (add more nodes or recreating cluster)

You just need to configure ```create-ami-skeleton.json``` file.

You can see all available options in ```create-ami-skeleton-example.json``` file.

_____


## * about k8s AMI:
### If you want to have a high available kubernetes cluster you must use somthings like RKE to deploy your k8s cluster on multiple masters (Kubeadm does not support multi master installation).

Full doc on: https://rancher.com/docs/rke/latest/en/example-yamls/

cluster.yml ex:

```
nodes:
    - address: 1.2.3.4
      user: ubuntu
      role:
        - controlplane
        - etcd
    
    - address: 1.2.3.5
      user: ubuntu
      role:
        - controlplane
        - etcd
    
    - address: 1.2.3.6
      user: ubuntu
      role:
        - worker

    - address: 1.2.3.7
      user: ubuntu
      role:
        - worker
```

_____


# How to create AMI (Amazon Machine Image) for traffic-generator and other services (ex: JMeter)

## Simpley replace pre requirements and service installation steps (JMeter in this case) in run-instances-skeleton.json, UserData section:

```
sudo apt-get update
sudo apt-get install -y openjdk-7-jdk
sudo apt-get install -y jmeter
sudo apt-get install -y unzip

wget http://jmeter-plugins.org/downloads/file/JMeterPlugins-Standard-1.2.0.zip
wget http://jmeter-plugins.org/downloads/file/JMeterPlugins-Extras-1.2.0.zip
wget http://jmeter-plugins.org/downloads/file/JMeterPlugins-ExtrasLibs-1.2.0.zip

sudo unzip JMeterPlugins-Standard-1.2.0.zip -d /usr/share/jmeter/
sudo unzip JMeterPlugins-Extras-1.2.0.zip -d /usr/share/jmeter/
sudo unzip JMeterPlugins-ExtrasLibs-1.2.0.zip -d /usr/share/jmeter/

```

## - Run the script again
```
./createAMI.sh
```

Now your envoiroment is ready for future use.

