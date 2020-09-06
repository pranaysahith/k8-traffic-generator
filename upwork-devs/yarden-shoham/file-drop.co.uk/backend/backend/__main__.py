from flask import Flask, request
from kubernetes import client, config
import os
import uuid
import json


def schedule(files):
    for file in files:
        file_identifier = f"file-drop-{uuid.uuid1()}"
        save_file(file, file_identifier)
        schedule_job_in_kubernetes(file, file_identifier)


def save_file(file, file_identifier):
    file.save(f"/usr/src/app/backend/static/{file_identifier}")


def schedule_job_in_kubernetes(file, file_identifier):
    job_name = file_identifier

    envs = [client.V1EnvVar(
            name="API_TOKEN", value=os.getenv("API_TOKEN")), client.V1EnvVar(
            name="TARGET", value=f"http://file-drop-traffic-generator-backend:5000/backend/static/{file_identifier}"), client.V1EnvVar(
            name="FILENAME", value=file.filename), client.V1EnvVar(
            name="API_URL", value=os.getenv("API_URL")
            )]

    processor_container = client.V1Container(
        name="processor",
        image=os.getenv("PROCESSOR_IMAGE"),
        env=envs)

    pod_spec = client.V1PodSpec(
        restart_policy="Never",
        containers=[processor_container])

    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(name=job_name, labels={
                                     "app": "file-drop-processor"}),
        spec=pod_spec)

    # Create the specification of the job
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=0)

    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_name),
        spec=spec)

    client.BatchV1Api().create_namespaced_job(
        body=job,
        namespace="default")


app = Flask(import_name=__name__, static_url_path="/backend/static")


@app.route("/backend/health")
def health():
    return ""


@app.route("/backend/pods/processor")
def processor_pods():
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(
        watch=False, label_selector="app=file-drop-processor")
    for i in ret.items:
        print("%s\t%s" %
              (i.status.phase, i.spec.containers[0].env[2].value), flush=True)
    return json.dumps([{"phase": i.status.phase, "filename": i.spec.containers[0].env[2].value} for i in ret.items])


@app.route("/backend/files", methods=["POST"])
def upload():
    uploaded_files = request.files.getlist("files[]")
    schedule(uploaded_files)
    return ""


if __name__ == '__main__':
    config.load_incluster_config()
    app.run(debug=True, host='0.0.0.0')
