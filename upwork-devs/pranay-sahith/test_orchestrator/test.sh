#!/bin/bash
set -e

num_of_users=${1-10}
test_id=${2-1005}
test_duration=${3-600}
release_name=traffic-generator

# deploy helm chart for each user in a loop
echo "Deploying traffic generator helm chart releases for ${num_of_users} users"
user_count=1
while [ $user_count -le $num_of_users ]; do
  user_name=${release_name}${user_count}
  kubectl get namespace ${user_name} || kubectl create namespace ${user_name}
  helm install --namespace ${user_name} ${user_name} \
    --set application.env.TEST_ID=${test_id} \
    chart/
  user_count=$(( user_count + 1 ))
done

# wait for test duration to complete
sleep $test_duration

# delete helm releases
user_count=1
while [ $user_count -le $num_of_users ]; do
  user_name=${release_name}${user_count}
  helm delete --namespace ${user_name} ${user_name}
  kubectl delete namespace ${user_name}
  user_count=$(( user_count + 1 ))
done
