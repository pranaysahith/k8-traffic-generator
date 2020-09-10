from unittest import TestCase
import asyncio
from traffic_generator import TrafficGenerator
from gw_file_drop import FileDrop
import logging
import os
import time

log = logging.getLogger("TG:gov_uk")
log.setLevel("INFO")


class TestGovUK(TestCase):

    @classmethod
    def setUpClass(cls):
        gov_uk_url = "https://www.gov.uk.glasswall-icap.com"
        tg = TrafficGenerator(gov_uk_url)
        # asyncio.get_event_loop().run_until_complete(tg.run(num_files=10))
        file_drop_url = "https://glasswall-file-drop.azurewebsites.net"
        cls.file_drop = FileDrop(file_drop_url)

    def test_is_clean(self):
        local_file_names = os.listdir(".")
        pdf_files = [f for f in local_file_names if f.rsplit(".")[-1] == "pdf" ]
        headless = True
        asyncio.get_event_loop().run_until_complete(self.file_drop.start(headless))
        for each_file in pdf_files:
            print(f"validating file: {each_file}")
            result = asyncio.get_event_loop().run_until_complete(self.file_drop.is_clean_file(each_file))
            print(each_file + ":" + result)
            assert result == "File is clean!"
            time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        asyncio.get_event_loop().run_until_complete(cls.file_drop.close_browser())
