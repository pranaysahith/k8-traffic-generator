import logging
import asyncio
import os
from traffic_generator import TrafficGenerator

log = logging.getLogger("GW:traffic_g")


class Main:
    @staticmethod
    def set_logging_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def run():
        Main.set_logging_level("INFO")
        asyncio.get_event_loop().run_until_complete(
            TrafficGenerator.run(
                url=os.getenv('URL'), action=os.getenv('ACTION'))
        )


if __name__ == "__main__":
    Main.run()
