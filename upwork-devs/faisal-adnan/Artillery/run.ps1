param ([string] $CONFIG_FILE, [int] $NUMBER_OF_JOBS)

if (-not (Test-Path $CONFIG_FILE)) {
    write-host "Config file $($CONFIG_FILE) does not exist"
    exit
}

if (-not (Test-Path "jobs")) {
    mkdir jobs
    write-host "Jobs directory has been created"
}

if (Test-Path ".\artillery-conf.yml") {
    rm ".\artillery-conf.yml"
    write-host "Previous version of the config file has been removed"
}

cp $CONFIG_FILE artillery-conf.yml

kubectl delete --ignore-not-found jobs -l jobgroup=artillery
kubectl delete --ignore-not-found secret artilleryconf
kubectl create secret generic artilleryconf --from-file=artillery-conf.yml

for ( $i = 0; $i -lt $NUMBER_OF_JOBS; $i++ ) {
    write-host "Submitting job $i"

    if (Test-Path ".\jobs\job-$i.yaml") {
        rm ".\jobs\job-$i.yaml"
    }

    ((Get-Content -path ".\artillery-job-tmpl.yaml" -Raw) -replace '\$NO', $i) | Set-Content -Path ".\jobs\job-$i.yaml"
    kubectl create -f .\jobs\job-$i.yaml
    rm ".\jobs\job-$i.yaml"
}
