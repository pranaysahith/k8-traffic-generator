import os
import logging
import logging.config
from pythonjsonlogger import jsonlogger
from datetime import datetime;
#import boto3
import requests
import time
import uuid
#from botocore.client import Config
#from botocore.exceptions import ClientError

from kubernetes import client, config

class ElkJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(ElkJsonFormatter, self).add_fields(log_record, record, message_dict)
#        log_record['@timestamp'] = datetime.now().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(uuid.uuid1().urn)

SRC_URL = os.getenv('SOURCE_MINIO_URL', 'http://192.168.99.120:30747')
SRC_ACCESS_KEY = os.getenv('SOURCE_MINIO_ACCESS_KEY', 'test')
SRC_SECRET_KEY = os.getenv('SOURCE_MINIO_SECRET_KEY', 'test@123')
SRC_BUCKET = os.getenv('SOURCE_MINIO_BUCKET', 'input')

TGT_URL = os.getenv('TARGET_MINIO_URL', 'http://192.168.99.120:31555')
TGT_ACCESS_KEY = os.getenv('TARGET_MINIO_ACCESS_KEY', 'test')
TGT_SECRET_KEY = os.getenv('TARGET_MINIO_SECRET_KEY', 'test@123')
TGT_BUCKET = os.getenv('TARGET_MINIO_BUCKET', 'output')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Main():

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def run_processor():
        job_name = uuid.uuid1().urn

        envs = [client.V1EnvVar(name="API_TOKEN", value=os.getenv("API_TOKEN")), 
                client.V1EnvVar(name="API_URL", value=os.getenv("API_URL")           
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
                                        "app": "file-rebuild-processor"}),
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

        while client.V1Job.status.active > 0:
            time.sleep(5)
            logger.info("Waiting for the job to complete");
            
        return

    @staticmethod
    def application():
        while True:
            try:
                Main.run_processor()
            except Exception as e:
                logger.error(e)

    @staticmethod
    def main():
        Main.log_level(LOG_LEVEL)
        if os.name != 'nt':
            os.system('service filebeat start')
        Main.application()

if __name__ == "__main__":
    Main.main()
