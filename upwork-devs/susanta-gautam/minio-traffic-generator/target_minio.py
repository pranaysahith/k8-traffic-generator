import os
import logging
import boto3
import requests
import time
from botocore.client import Config
from botocore.exceptions import ClientError
from threading import Thread

logger = logging.getLogger('GW:minio')
file_path = '/files/'


class Main():

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def download_from_minio(UPLOAD_TO_TARGET):
        URL = os.getenv('SOURCE_MINIO_URL', 'http://source-minio:9000')
        ACCESS_KEY = os.getenv('SOURCE_MINIO_ACCESS_KEY', 'susanta')
        SECRET_KEY = os.getenv('SOURCE_MINIO_SECRET_KEY', 'susanta@123')
        BUCKET = os.getenv('SOURCE_MINIO_BUCKET', 'dummy')

        try:
            s3 = boto3.resource('s3', endpoint_url=URL, aws_access_key_id=ACCESS_KEY,
                                aws_secret_access_key=SECRET_KEY, config=Config(signature_version='s3v4'))
            logger.debug('Check if the Bucket {} exists'.format(BUCKET))
            if (s3.Bucket(BUCKET) in s3.buckets.all()):
                logger.debug(
                    'Bucket {} found. Starting to download files from it.'.format(BUCKET))
                bucket = s3.Bucket(BUCKET)
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
        except e:
            logger.error(e)

    @staticmethod
    def upload_to_minio(file_path, filename):
        URL = os.getenv('TARGET_MINIO_URL', 'http://target-minio:9000')
        ACCESS_KEY = os.getenv('TARGET_MINIO_ACCESS_KEY', 'susanta')
        SECRET_KEY = os.getenv('TARGET_MINIO_SECRET_KEY', 'susanta@123')
        BUCKET = os.getenv('TARGET_MINIO_BUCKET', 'dummy')

        try:
            s3 = boto3.resource('s3', endpoint_url=URL, aws_access_key_id=ACCESS_KEY,
                                aws_secret_access_key=SECRET_KEY, config=Config(signature_version='s3v4'))
            logger.debug(
                'Checking if the Bucket to upload files exists or not.')
            if (s3.Bucket(BUCKET) in s3.buckets.all()) == False:
                logger.info('Bucket not Found. Creating Bucket.')
                s3.create_bucket(Bucket=BUCKET)
            logger.debug(
                'Uploading file to bucket {} minio {}'.format(BUCKET, URL))
            file_to_upload = file_path + filename
            s3.Bucket(BUCKET).upload_file(file_to_upload, filename)
        except ClientError as e:
            logger.error(
                "Cannot connect to the minio {}. Please vefify the Credentials.".format(URL))
        except e:
            logger.error(e)

    @staticmethod
    def application():
        UPLOAD_TO_TARGET = os.getenv('UPLOAD_TO_TARGET', 'false')
        IN_LOOP = os.getenv('IN_LOOP', 'FALSE')
        endpoint = '/minio/health/ready'
        logger.info('Checking if the Target Minio {} is avaliable.'.format(
            os.getenv('TARGET_MINIO_URL')))
        if UPLOAD_TO_TARGET.upper() == 'TRUE':
            URL = os.getenv('TARGET_MINIO_URL') + endpoint

            for i in range(0, 4):
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

        for j in range(0, 4):
            URL = os.getenv('SOURCE_MINIO_URL') + endpoint
            logger.info('Checking if the Source Minio {} is avaliable.'.format(
                os.getenv('SOURCE_MINIO_URL')))
            try:
                response2 = requests.get(URL, timeout=2)
                if response2.status_code == 200:
                    logger.info('Recieved status code {} from Minio {}.'.format(
                        response2.status_code, URL))
                    if IN_LOOP.upper() == 'TRUE':
                        logger.info('Starting Application in Loop Mode.')
                        while True:
                            Main.download_from_minio(UPLOAD_TO_TARGET)
                    else:
                        Main.download_from_minio(UPLOAD_TO_TARGET)
                else:
                    if j == 4:
                        logger.error(
                            'Could not connect to the Soruce Minio {}.'.format(URL))
                        exit(1)
            except:
                logger.error('Could not connect to Minio {}'.format(URL))

    @staticmethod
    def main():
        LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
        Main.log_level(LOG_LEVEL)
        time.sleep(5)
        Main.application()


if __name__ == "__main__":
    Main.main()
