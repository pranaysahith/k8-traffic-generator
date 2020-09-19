# How to create AMI (Amazon Machine Image) for k8s

<img src="https://d39w7f4ix9f5s9.cloudfront.net/dims4/default/f41a71b/2147483647/strip/true/crop/1200x542+0+44/resize/1440x650!/quality/90/?url=http%3A%2F%2Famazon-blogs-brightspot.s3.amazonaws.com%2F40%2Fb0%2F16d665224675bf7ecf4431d1e9ca%2Faws-logo-smile-1200x630.png" alt="Diagram" width="500"/>

_____

An Amazon Machine Image (AMI) provides the information required to launch an instance. You must specify an AMI when you launch an instance. You can launch multiple instances from a single AMI when you need multiple instances with the same configuration. You can use different AMIs to launch instances when you need instances with different configurations.

_____


If you want to run traffic-generator on K8S infrastructure, the best way to do that is to create EKS (Elastic Kubernetes Service). Amazon Elastic Kubernetes Service is a fully managed Kubernetes service. Customers such as Intel, Snap, Intuit, GoDaddy, and Autodesk trust EKS to run their most sensitive and mission critical applications because of its security, reliability, and scalability.
EKS souuports ASG (Auto Scaling Groups) to provide auto scale in workers level but still you want to manage your own bare-metal K8S service you must create an AMI for your EC2 instances because all workers and masters deployed on EC2 instances. 

_____


## 1. First Create 2 EC2 Instances (one master and one worker)

Full doc on: https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html

_____


## 2. Install pre requirements

```
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

sudo swapon -s
sudo swapoff -a

# To disable the SWAP permanently, we need to edit the '/etc/fstab' file.
sudo vim /etc/fstab
# Make a comment on the SWAP partition type.
#/dev/mapper/hakase--labs--vg-swap_1 none            swap    sw              0       0

sudo apt install -y apt-transport-https
sudo reboot
```

_____


## 3. Now it's time to make an AMI image for future use (add more nodes or recreating cluster)

- open EC2 managment pannel

- Right-click the instance you want to use as the basis for your AMI, and choose Create Image from the context menu.
<img src="https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/images/tkv-ec2-create-ami-menu2.png" alt="Diagram" width="300"/>

- In the Create Image dialog box, type a unique name and description, and then choose Create Image. By default, Amazon EC2 shuts down the instance, takes snapshots of any attached volumes, creates and registers the AMI, and then reboots the instance. Choose No rebootif you don't want your instance to be shut down.

- It may take a few minutes for the AMI to be created. After it is created, it will appear in the AMIs view in AWS Explorer. To display this view, double-click the Amazon EC2 | AMIs node in AWS Explorer. To see your AMIs, from the Viewing drop-down list, choose Owned By Me. You may need to choose Refresh to see your AMI. When the AMI first appears, it may be in a pending state, but after a few moments, it transitions to an available state.

Now your custom AMI for bare-metal k8s is ready!
_____


## 4. If you want to have a high available kubernetes cluster you must use somthings like RKE to deploy your k8s cluster on multiple masters (Kubeadm does not support multi master installation).

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

## 1. First Create an EC2 Instance

Full doc on: https://docs.aws.amazon.com/efs/latest/ug/gs-step-one-create-ec2-resources.html

_____


## 2. Install pre requirements and service (JMeter in this case)

```
#Prepare environment
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

# Change heap for jmeter
vi /usr/share/jmeter/bin/jmeter
# run_java -Xms4096m -Xmx4096m -Djmeter.home=/usr/share/jmeter org.apache.jmeter.NewDriver "$@"

# Upload jms file to server
scp -i <path_to_key> <path_to_local_file> <user>@<server_url>:<path_on_server>

# Run jmeter without GUI
cd /usr/share/jmeter/bin/
./jmeter -n -t <absolute_path_to_jmx> -l <absolute_path_to_jtl>

# Download results
scp -i <path_to_key> <user>@<server_url>:<path_on_server> <path_to_local_file>
```

Now your envoiroment is ready for future use.

_____


## 3. Now it's time to make an AMI image for future use (add more nodes or recreating JMeter)

- open EC2 managment pannel

- Right-click the instance you want to use as the basis for your AMI, and choose Create Image from the context menu.
<img src="https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/images/tkv-ec2-create-ami-menu2.png" alt="Diagram" width="300"/>

- In the Create Image dialog box, type a unique name and description, and then choose Create Image. By default, Amazon EC2 shuts down the instance, takes snapshots of any attached volumes, creates and registers the AMI, and then reboots the instance. Choose No rebootif you don't want your instance to be shut down.

- It may take a few minutes for the AMI to be created. After it is created, it will appear in the AMIs view in AWS Explorer. To display this view, double-click the Amazon EC2 | AMIs node in AWS Explorer. To see your AMIs, from the Viewing drop-down list, choose Owned By Me. You may need to choose Refresh to see your AMI. When the AMI first appears, it may be in a pending state, but after a few moments, it transitions to an available state.

Now your custom AMI for JMeter is ready!

