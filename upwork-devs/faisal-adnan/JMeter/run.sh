#!/bin/sh
CONFIG_FILE=$1
NUMBER_OF_JOBS=$2

mkdir -p jmeter-jobs

[ -f "jmeter-conf.yml" ] && rm jmeter-conf.gmx
cp $CONFIG_FILE jmeter-conf.gmx

kubectl delete --ignore-not-found jobs -l jobgroup=jmeter
kubectl delete --ignore-not-found secret jmeterconf
kubectl create secret generic jmeterconf --from-file=jmeter-conf.gmx

START=1
for (( c=$START; c<=$NUMBER_OF_JOBS; c++ ))
do
    echo "Submitting job $c"
    cat jmeter-job-tmpl.yaml | sed "s/\$NO/$c/" > ./jmeter-jobs/job-$c.yaml
    kubectl create -f ./jmeter-jobs/job-$c.yaml
    rm ./jmeter-jobs/job-$c.yaml
done
