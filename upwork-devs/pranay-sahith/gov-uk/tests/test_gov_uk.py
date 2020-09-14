from unittest import TestCase
import asyncio
import logging
import os
import time
import sys
from uuid import uuid4
from tika import parser
from traffic_generator import TrafficGenerator
from gw_file_drop import FileDrop
from elastic_service import ElasticService
from datetime import datetime

log = logging.getLogger("TG:gov_uk")
log.setLevel(logging.INFO)
logging.basicConfig( stream=sys.stdout )


class TestGovUK(TestCase):

    @classmethod
    def setUpClass(cls):
        gov_uk_url = os.getenv("GOV_UK_URL", "https://www.gov.uk.glasswall-icap.com")
        file_drop_url = os.getenv("FILE_DROP_URL", "https://glasswall-file-drop.azurewebsites.net")
        num_files = int(os.getenv("NUM_FILES", 1))
        elastic_host = os.getenv("ELASTIC_HOST", "localhost")
        elastic_port = os.getenv("ELASTIC_PORT", "9200")
        elastic_username = os.getenv("ELASTIC_USER")
        elastic_password = os.getenv("ELASTIC_PASSWORD")
        index_name = os.getenv("INDEX_NAME", "tg_test_results")
        tg = TrafficGenerator(gov_uk_url)
        asyncio.get_event_loop().run_until_complete(tg.run(num_files=num_files))
        cls.file_drop = FileDrop(file_drop_url)
        cls.ship_test_results_to_elastic = os.getenv("SHIP_TO_ELASTIC", "0")
        if cls.ship_test_results_to_elastic == "1":
            cls.es = ElasticService(elastic_host, elastic_port, elastic_username, elastic_password)
            cls.es.create_index(index_name)

    def test_is_clean(self):
        guid = uuid4()
        start_time = datetime.now()
        try:
            local_file_names = os.listdir(".")
            pdf_files = [f for f in local_file_names if f.rsplit(".")[-1] == "pdf" ]
            headless = bool(os.getenv("HEADLESS", 1))
            asyncio.get_event_loop().run_until_complete(self.file_drop.start(headless))
            for each_file in pdf_files:
                log.info(f"validating file: {each_file}")
                result = asyncio.get_event_loop().run_until_complete(self.file_drop.is_clean_file(each_file))
                log.info(each_file + ": " + result)
                assert result == "File is clean!"
                time.sleep(3)

            if self.ship_test_results_to_elastic:
                end_time = datetime.now()
                test_duration = (end_time - start_time).microseconds
                test_results = {
                    "testId": guid,          
                    "start": start_time,                 
                    "end": end_time,
                    "testDuration": test_duration, 
                    "testScenarionName": "TestGovUK",
                    "testScenarionId": "1",
                    "testStepNo": 1,
                    "testStepName": "test_is_clean",
                    "testDocUrl": None,
                    "result": "success",
                    "error": None,
                    "errorMessage": None,
                }
                self.es.create_doc(self.index_name, guid, test_results)
        except Exception as e:
            log.error(e)
            if self.ship_test_results_to_elastic:
                end_time = datetime.now()
                test_duration = (end_time - start_time).microseconds
                test_results = {
                    "testId": guid,          
                    "start": start_time,                 
                    "end": end_time,
                    "testDuration": test_duration,
                    "testScenarionName": "TestGovUK",
                    "testScenarionId": "1",
                    "testStepNo": 1,
                    "testStepName": "test_is_clean",
                    "testDocUrl": None,
                    "result": "fail",
                    "error": None,
                    "errorMessage": str(e),
                }
                self.es.create_doc(self.index_name, guid, test_results)


    def test_tag(self):
        guid = uuid4()
        start_time = datetime.now()
        try:
            local_file_names = os.listdir(".")
            pdf_files = [f for f in local_file_names if f.rsplit(".")[-1] == "pdf" ]
            for each_file in pdf_files:
                raw = parser.from_file(each_file)
                log.info(f"parsed file: {each_file}")
                assert "Glasswall Approved" in raw["content"]
            
            if self.ship_test_results_to_elastic:
                end_time = datetime.now()
                test_duration = (end_time - start_time).microseconds
                test_results = {
                    "testId": guid,          
                    "start": start_time,                 
                    "end": end_time,
                    "testDuration": test_duration, 
                    "testScenarionName": "TestGovUK",
                    "testScenarionId": "1",
                    "testStepNo": 2,
                    "testStepName": "test_tag",
                    "testDocUrl": None,
                    "result": "success",
                    "error": None,
                    "errorMessage": None,
                }
                self.es.create_doc(self.index_name, guid, test_results)
        except Exception as e:
            log.error(e)
            if self.ship_test_results_to_elastic:
                end_time = datetime.now()
                test_duration = (end_time - start_time).microseconds
                test_results = {
                    "testId": guid,          
                    "start": start_time,                 
                    "end": end_time,
                    "testDuration": test_duration,
                    "testScenarionName": "TestGovUK",
                    "testScenarionId": "1",
                    "testStepNo": 2,
                    "testStepName": "test_tag",
                    "testDocUrl": None,
                    "result": "fail",
                    "error": str(e),
                    "errorMessage": str(e),
                }
                self.es.create_doc(self.index_name, guid, test_results)

    @classmethod
    def tearDownClass(cls):
        asyncio.get_event_loop().run_until_complete(cls.file_drop.close_browser())
