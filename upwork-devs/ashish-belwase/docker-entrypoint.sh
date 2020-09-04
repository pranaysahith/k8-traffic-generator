#!/bin/bash
set -e

cd /usr/src/app
if [ "$MODE" = "traffic" ]
then
    exec python main.py
elif [ "$MODE" = "testing" ]
then
    exec python -m unittest
else
    echo "Invalid mode"
fi