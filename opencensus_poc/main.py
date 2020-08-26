import argparse
import logging
import asyncio
import os
from traffic_generator import TrafficGenerator

log = logging.getLogger("GW:traffic_g")


def set_logging_level(level):
    logging.basicConfig(level=getattr(logging, level))


def main():
    set_logging_level("INFO")
    url = os.getenv("BASE_URL", "https://glasswallsolutions.com")
    asyncio.get_event_loop().run_until_complete(
        TrafficGenerator.run(url)
    )


if __name__ == "__main__":
    main()
