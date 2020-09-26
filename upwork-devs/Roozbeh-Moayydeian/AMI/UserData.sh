#!/bin/bash -xe

exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
apt update
apt install apt-transport-https docker.io -y
systemctl start docker
systemctl enable docker
swapon -s
swapoff -a
shutdown -h now
