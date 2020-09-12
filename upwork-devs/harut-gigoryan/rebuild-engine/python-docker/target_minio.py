#import pdb
import os
import logging
import logging.config
from pythonjsonlogger import jsonlogger
from datetime import datetime;
import boto3
import requests
import time
import uuid
from botocore.client import Config
from botocore.exceptions import ClientError
from threading import Thread
from minio import Minio
from minio.error import ResponseError

#logger = logging.getLogger('minio')

class ElkJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(ElkJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['@timestamp'] = datetime.now().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(uuid.uuid1().urn)

logging.info('Application running!')

file_path = '/files/'

SRC_URL = os.getenv('SOURCE_MINIO_URL', 'http://192.168.99.115:32580')
SRC_ACCESS_KEY = os.getenv('SOURCE_MINIO_ACCESS_KEY', 'minio1')
SRC_SECRET_KEY = os.getenv('SOURCE_MINIO_SECRET_KEY', 'minio1@123')
SRC_BUCKET = os.getenv('SOURCE_MINIO_BUCKET', 'dummy')

TGT_URL = os.getenv('TARGET_MINIO_URL', 'http://192.168.99.115:31634')
TGT_ACCESS_KEY = os.getenv('TARGET_MINIO_ACCESS_KEY', 'minio2')
TGT_SECRET_KEY = os.getenv('TARGET_MINIO_SECRET_KEY', 'minio2@123')
TGT_BUCKET = os.getenv('TARGET_MINIO_BUCKET', 'dummy')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
UPLOAD_TO_TARGET = os.getenv('UPLOAD_TO_TARGET', 'TRUE')
IN_LOOP = os.getenv('IN_LOOP', 'TRUE')

class Main():

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def download_from_minio(UPLOAD_TO_TARGET):

        try:
            s3 = boto3.resource('s3', endpoint_url=SRC_URL, aws_access_key_id=SRC_ACCESS_KEY,
                                aws_secret_access_key=SRC_SECRET_KEY, config=Config(signature_version='s3v4'))
            logger.debug('Check if the Bucket {} exists'.format(SRC_BUCKET))
            if (s3.Bucket(SRC_BUCKET) in s3.buckets.all()):
                logger.debug(
                    'Bucket {} found. Starting to download files from it.'.format(SRC_BUCKET))
                bucket = s3.Bucket(SRC_BUCKET)
                for files in bucket.objects.all():
                    path, filename = os.path.split(files.key)
                    obj_file = file_path + filename
                    logger.debug('Downloading file {}.'.format(filename))
                    bucket.download_file(files.key, obj_file)
                    if UPLOAD_TO_TARGET.upper() == 'TRUE':
                        logger.debug(
                            'Calling function to upload the file {} to next minio.'.format(filename))
                        Main.upload_to_minio(file_path, filename)

        except ClientError as e:
            logger.error(
                "Cannot Connect to the Minio {}. Please Verify your credentials.".format(URL))
        except Exception as e:
            logger.error(e)

    @staticmethod
    def upload_to_minio(file_path, filename):

        try:
            s3 = boto3.resource('s3', endpoint_url=TGT_URL, aws_access_key_id=TGT_ACCESS_KEY,
                                aws_secret_access_key=TGT_SECRET_KEY, config=Config(signature_version='s3v4'))
            logger.debug(
                'Checking if the Bucket to upload files exists or not.')
            if (s3.Bucket(TGT_BUCKET) in s3.buckets.all()) == False:
                logger.info('Bucket not Found. Creating Bucket.')
                s3.create_bucket(Bucket=TGT_BUCKET)
            logger.debug(
                'Uploading file to bucket {} minio {}'.format(TGT_BUCKET, TGT_URL))
            file_to_upload = file_path + filename
            s3.Bucket(TGT_BUCKET).upload_file(file_to_upload, filename)
        except ClientError as e:
            logger.error(
                "Cannot connect to the minio {}. Please vefify the Credentials.".format(TGT_URL))
        except Exception as e:
            logger.info(e)

    @staticmethod
    def application():
        endpoint = '/minio/health/ready'
        logger.info('Checking if the Target Minio {} is avaliable.'.format(TGT_URL))
        if UPLOAD_TO_TARGET.upper() == 'TRUE':
            URL = TGT_URL + endpoint

            for i in range(0, 1):
                try:
                    response = requests.get(URL, timeout=2)
                    if response.status_code == 200:
                        logger.info('Recieved Response code {} from {}'.format(
                            response.status_code, URL))
                        break
                    else:
                        if i == 3:
                            logger.error(
                                'Could Not connect to Target Minio {}.'.format(URL))
                            exit(2)
                except:
                    logger.error(
                        'Could not connect to Target Minio {}.'.format(URL))

        for j in range(0, 1):
            URL = SRC_URL + endpoint
            logger.info('Checking if the Source Minio {} is avaliable.'.format(SRC_URL))
            try:
                response2 = requests.get(URL, timeout=2)
                if response2.status_code == 200:
                    logger.info('Recieved status code {} from Minio {}.'.format(
                        response2.status_code, URL))
                    Main.download_from_minio(UPLOAD_TO_TARGET)
#                    
                    if IN_LOOP.upper() == 'TRUE':
##                        pdb.set_trace()
                        logger.info('Starting Application in Loop Mode.')
                        while True:
                            Main.download_from_minio(UPLOAD_TO_TARGET)
#                       
                else:
                    if j == 4:
                        logger.error(
                            'Could not connect to the Soruce Minio {}.'.format(URL))
                        exit(1)
            except:
                logger.error('Could not connect to Minio {}'.format(URL))

    @staticmethod
    def main():
#        pdb.set_trace()
        Main.log_level(LOG_LEVEL)
        time.sleep(5)
        if os.name == 'nt':
            file_path = 'C:/files/'
        else:
            os.system('service filebeat start')
        Main.application()


if __name__ == "__main__":
    Main.main()
