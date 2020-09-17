from kubernetes import client, config
from minio import Minio
import os
import uuid


def dispatch(endpoint, access_key, secret_key, bucket_name, object_name):
    job_name = f"local-rebuild-{uuid.uuid1()}"

    downloader_env = [
        client.V1EnvVar(name="ENDPOINT", value=endpoint),
        client.V1EnvVar(name="ACCESS_KEY", value=access_key),
        client.V1EnvVar(name="SECRET_KEY", value=secret_key),
        client.V1EnvVar(name="BUCKET_NAME", value=bucket_name),
        client.V1EnvVar(name="OBJECT_NAME", value=object_name)
    ]

    downloader_container = client.V1Container(
        name="downloader",
        image=os.getenv("DOWNLOADER_IMAGE"),
        env=downloader_env,
        volume_mounts=[client.V1VolumeMount(
            name="processor-input", mount_path="/output")])

    processor_container = client.V1Container(
        name="processor",
        image=os.getenv("PROCESSOR_IMAGE"),
        volume_mounts=[client.V1VolumeMount(name="processor-input", mount_path="/input", read_only=True),
                       client.V1VolumeMount(name="processor-output", mount_path="/output")])

    pod_spec = client.V1PodSpec(
        restart_policy="Never",
        init_containers=[downloader_container],
        containers=[processor_container],
        volumes=[
            client.V1Volume(name="processor-input",
                            empty_dir=client.V1EmptyDirVolumeSource()),
            client.V1Volume(name="processor-output",
                            empty_dir=client.V1EmptyDirVolumeSource()),
        ])

    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(name=job_name, labels={
                                     "app": "local-rebuild-processor"}),
        spec=pod_spec)

    # Create the specification of the job
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=0)

    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_name, labels={
                                     "app": "local-rebuild-processor"}),
        spec=spec)

    client.BatchV1Api().create_namespaced_job(
        body=job,
        namespace="default")


if __name__ == "__main__":
    endpoint = os.getenv("ENDPOINT")
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    bucket_name = os.getenv("BUCKET_NAME")

    config.load_incluster_config()

    s3client = Minio(endpoint=endpoint, access_key=access_key,
                     secret_key=secret_key)
    objects = s3client.list_objects(
        bucket_name=bucket_name, recursive=True)
    for object in objects:
        print(object.object_name)
        dispatch(endpoint=endpoint, access_key=access_key, secret_key=secret_key,
                 bucket_name=bucket_name, object_name=object.object_name)
