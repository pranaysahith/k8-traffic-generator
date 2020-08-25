import logging
from pyppeteer import launch
from pyquery import PyQuery as pq
import urllib.request
from datetime import datetime

log = logging.getLogger("GW:traffic_g")


class TrafficGenerator:
    Allowed_Methods = ["open", "follow", "download", "upload"]

    @staticmethod
    async def open(page, url):
        await page.goto(url)
        log.info(f"loaded url : {url}")

    @staticmethod
    async def follow(page, url):
        pass

    @staticmethod
    async def download(page, url):
        await page.goto(url)
        doc = pq(await page.content())
        pdfs = doc.find('a[href*=".pdf"]')
        log.info("downloading {} pdfs".format(len(pdfs)))
        for pdf in pdfs:
            url = pdf.get("href")
            with urllib.request.urlopen(url) as f:
                f.read()

    @staticmethod
    async def upload(page, url, data={}):
        pass

    @staticmethod
    async def run(url, action):
        if action not in TrafficGenerator.Allowed_Methods:
            log.info(f"Invalid action : {action}")

        log.info(f"starting traffic on : {url} , action: {action}")
        browser = await launch()

        page = await browser.newPage()
        m = getattr(TrafficGenerator, action)
        await m(page, url)
        await browser.close()
