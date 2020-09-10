from unittest import TestCase
import asyncio
import logging
import os
import time
from tika import parser
from traffic_generator import TrafficGenerator
from gw_file_drop import FileDrop

log = logging.getLogger("TG:gov_uk")
log.setLevel("INFO")


class TestGovUK(TestCase):

    @classmethod
    def setUpClass(cls):
        gov_uk_url = os.getenv("GOV_UK_URL", "https://www.gov.uk.glasswall-icap.com")
        file_drop_url = os.getenv("FILE_DROP_URL", "https://glasswall-file-drop.azurewebsites.net")
        num_files = int(os.getenv("NUM_FILES", 10))
        tg = TrafficGenerator(gov_uk_url)
        asyncio.get_event_loop().run_until_complete(tg.run(num_files=num_files))
        cls.file_drop = FileDrop(file_drop_url)

    def test_is_clean(self):
        local_file_names = os.listdir(".")
        pdf_files = [f for f in local_file_names if f.rsplit(".")[-1] == "pdf" ]
        headless = bool(os.getenv("HEADLESS", 1))
        asyncio.get_event_loop().run_until_complete(self.file_drop.start(headless))
        for each_file in pdf_files:
            print(f"validating file: {each_file}")
            result = asyncio.get_event_loop().run_until_complete(self.file_drop.is_clean_file(each_file))
            print(each_file + ":" + result)
            assert result == "File is clean!"
            time.sleep(3)

    def test_tag(self):
        local_file_names = os.listdir(".")
        pdf_files = [f for f in local_file_names if f.rsplit(".")[-1] == "pdf" ]
        for each_file in pdf_files:
            raw = parser.from_file(each_file)
            print(f"parsed file: {each_file}")
            assert "Glasswall Approved" in raw["content"]

    @classmethod
    def tearDownClass(cls):
        asyncio.get_event_loop().run_until_complete(cls.file_drop.close_browser())
