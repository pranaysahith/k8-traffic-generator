#!/bin/sh
set -e

mc alias set target $PROTOCOL://$ENDPOINT $ACCESS_KEY $SECRET_KEY
exec mc cp "target/$BUCKET_NAME/$OBJECT_NAME" /output/