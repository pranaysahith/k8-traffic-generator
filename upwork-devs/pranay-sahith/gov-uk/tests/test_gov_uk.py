from unittest import TestCase
import asyncio
import time
from traffic_generator import TrafficGenerator
from gw_file_drop import FileDrop


class TestGovUK(TestCase):

    @classmethod
    def setUp(cls):
        gov_uk_url = "https://www.gov.uk.glasswall-icap.com"
        tg = TrafficGenerator(gov_uk_url)
        asyncio.get_event_loop().run_until_complete(tg.run())
        file_drop_url = "https://glasswall-file-drop.azurewebsites.net"
        cls.file_drop = FileDrop(file_drop_url)

    def test_is_clean(self):
        local_file_names = [
        ]
        
        headless = True
        asyncio.get_event_loop().run_until_complete(self.file_drop.start(headless))
        for each_file in local_file_names:
            result = asyncio.get_event_loop().run_until_complete(self.file_drop.is_clean_file(each_file))
            print(result)
            assert result == "File is clean!"
            time.sleep(3)

    @classmethod
    def tearDown(cls):
        asyncio.get_event_loop().run_until_complete(cls.file_drop.close_browser())
