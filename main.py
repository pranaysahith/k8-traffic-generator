import argparse
import logging
import asyncio
from traffic_generator import TrafficGenerator

log = logging.getLogger("GW:traffic_g")


def get_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        "-u",
        dest="url",
        help="Url of site to load traffic.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--action",
        "-a",
        dest="action",
        help="Action to perform.",
        type=str,
        required=False,
    )
    return parser.parse_args()


def set_logging_level(level):
    logging.basicConfig(level=getattr(logging, level))


def main():
    args = get_command_line_args()
    set_logging_level("INFO")
    asyncio.get_event_loop().run_until_complete(
        TrafficGenerator.run(url=args.url, action=args.action)
    )


if __name__ == "__main__":
    main()
