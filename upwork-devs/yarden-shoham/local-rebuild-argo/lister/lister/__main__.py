from minio import Minio
import os
import json
import sys

if __name__ == "__main__":
    endpoint = os.getenv("ENDPOINT")
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    bucket_name = os.getenv("BUCKET_NAME")

    s3client = Minio(endpoint=endpoint, access_key=access_key,
                     secret_key=secret_key)
    objects = s3client.list_objects(
        bucket_name=bucket_name, recursive=True)

    json.dump([object.object_name for object in objects], sys.stdout)
