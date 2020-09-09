import logging
import asyncio
import os
import time
from pprint import pprint
from opencensus_prometheus import OpenCensusPrometheus
from traffic_generator import TrafficGenerator


class Main():
    log = logging.getLogger("GW:traffic_g")

    @staticmethod
    def set_logging_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def main():
        Main.set_logging_level("INFO")
        url = os.getenv("BASE_URL", "http://localhost:9090/")
        username = os.getenv("NC_USER")
        password = os.getenv("NC_PASSWORD")
        headless = bool(os.getenv("HEADLESS", 1))
        test_id = os.getenv("TEST_ID", "1001")
        ocp = OpenCensusPrometheus(test_id)
        tg = TrafficGenerator(url, ocp, username, password, headless)
        while True:
            try:
                asyncio.get_event_loop().run_until_complete(
                    tg.run()
                )
            except Exception as e:
                Main.log.error(str(e))
            break


if __name__ == "__main__":
    Main.main()
