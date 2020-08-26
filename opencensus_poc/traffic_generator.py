import logging
from pyppeteer import launch
from pyquery import PyQuery as pq
import urllib.request
from datetime import datetime

log = logging.getLogger("GW:traffic_g")


class TrafficGenerator:

    @staticmethod
    async def home_page(page, url):
        await page.goto(url)
        log.info(f"loaded url : {url}")


    @staticmethod
    async def download_brochure(page, url):
        await page.goto(url + "/technology")
        doc = pq(await page.content())
        pdfs = doc.find('a[href*=".pdf"]')
        urls = set([pdf.get("href") for pdf in pdfs])
        log.info("downloading {} pdfs".format(len(urls)))
        for url in urls:
            with urllib.request.urlopen(url) as f:
                log.info(f"downloading pdf: {url}")
                pdf_content = f.read()
                with open(url.split("/")[-1], "wb") as f_writer:
                    f_writer.write(pdf_content)

    @staticmethod
    async def run(url):

        log.info(f"starting traffic on : {url}")
        browser = await launch(headless=False)

        page = await browser.newPage()
        m = getattr(TrafficGenerator, "home_page")
        await m(page, url)
        m = getattr(TrafficGenerator, "download_brochure")
        await m(page, url)
        await browser.close()
