import os
import asyncio
from traffic_generator import TrafficGenerator


class Main():

    @staticmethod
    def main():
        url = os.getenv("TARGET_URL")
        tg = TrafficGenerator(url)
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_until_complete(
            # tg.run()
        # )
        asyncio.run(tg.run())


if __name__ == "__main__":
    Main.main()
