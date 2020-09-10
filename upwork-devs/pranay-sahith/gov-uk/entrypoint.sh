#!/bin/bash

set -e
cd /app/tests
export PYTHONPATH=$(pwd)/..
python -m unittest
