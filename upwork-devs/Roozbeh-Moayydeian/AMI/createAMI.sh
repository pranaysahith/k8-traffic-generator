# !/bin/bash

# Fill default values
KEY_NAME=${1:-"roozbeh"}
BASE_IMAGEID=${2:-"ami-0dba2cb6798deb6d8"}
SECURITY_GROUP=${3:-"testing-kubernetes"}
INSTANCE_NAME=${4:-"AMItest"}
INSTANCE_TYPE=${5:-"t2.micro"}
AMI_NAME=${6:-"gw-ami-test"}

if [[ $KEY_NAME == --help ]]
then
    echo "Please set your parameters as metioned below"
    echo "./createAMI.sh KEY_NAME BASE_IMAGEID SECURITY_GROUP INSTANCE_NAME INSTANCE_TYPE AMI_NAME"
    exit 0
fi

echo "KEY_NAME: ${KEY_NAME}"
echo "BASE_IMAGEID: ${BASE_IMAGEID}"
echo "SECURITY_GROUP: ${SECURITY_GROUP}"
echo "INSTANCE_NAME: ${INSTANCE_NAME}"
echo "INSTANCE_TYPE: ${INSTANCE_TYPE}"
echo "AMI_NAME: ${AMI_NAME}"

# Generating instance skeleton
cp ./run-instances-skeleton.json ./run-instances-skeleton-out.json
sed -i "s/KEY_NAME/${KEY_NAME}/g" ./run-instances-skeleton-out.json
sed -i "s/INSTANCE_TYPE/${INSTANCE_TYPE}/g" ./run-instances-skeleton-out.json
sed -i "s/BASE_IMAGEID/${BASE_IMAGEID}/g" ./run-instances-skeleton-out.json
sed -i "s/SECURITY_GROUP/${SECURITY_GROUP}/g" ./run-instances-skeleton-out.json
sed -i "s/INSTANCE_NAME/${INSTANCE_NAME}/g" ./run-instances-skeleton-out.json
sed -i "s/AMI_NAME/${AMI_NAME}/g" ./run-instances-skeleton-out.json

# Create instance
INSTANCE_ID=$(aws ec2 run-instances --region us-east-1 --output json --cli-input-json file://run-instances-skeleton-out.json | jq -r '.Instances[0].InstanceId')

# Check if instance creation is successful
if [[ $INSTANCE_ID == i-* ]]
then
    echo "Creating AMI from instance: ${INSTANCE_ID}"
else
    echo "aws ec2 run-instances --region us-east-1 --output json --cli-input-json file://run-instances-skeleton.json"
    exit 1
fi

# Wait for userData execution
echo "Wait for userData execution (180s)"
sleep 180
echo "Start creating AMI"

# Generating AMI skeleton
cp ./create-ami-skeleton.json ./create-ami-skeleton-out.json
sed -i "s/INSTANCE_ID/${INSTANCE_ID}/g" ./create-ami-skeleton-out.json

# Create AMI based on instance
aws ec2 create-image --region us-east-1 --output json --cli-input-json file://create-ami-skeleton-out.json

echo "done"
