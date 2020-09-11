#!/bin/bash

set -e
cd /app/tests
export PYTHONPATH=$(pwd)/..
if [ "$LOOP" -ne "1" ]; then
  python -m unittest
else
  runtime="${RUN_FOR_MINS} minute"
  endtime=$(date -ud "$runtime" +%s)
  while [[ $(date -u +%s) -le $endtime ]]
  do
      python -m unittest
  done
fi
