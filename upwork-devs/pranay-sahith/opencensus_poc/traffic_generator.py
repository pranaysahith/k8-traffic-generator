import logging
from pyppeteer import launch
from pyquery import PyQuery as pq
import urllib.request
from datetime import datetime
import os


log = logging.getLogger("GW:traffic_g")


class TrafficGenerator:

    @staticmethod
    async def home_page(page, url, ocp):
        then = datetime.now()
        await page.goto(url)
        now = datetime.now()
        time_taken = now - then
        ocp.set_measurement("home_page", int(time_taken.total_seconds()))
        log.info(f"loaded url : {url}")


    @staticmethod
    async def download_brochure(page, url, ocp):
        then = datetime.now()
        await page.goto(url + "/technology")
        doc = pq(await page.content())
        pdfs = doc.find('a[href*=".pdf"]')
        urls = set([pdf.get("href") for pdf in pdfs])
        log.info("downloading {} pdfs".format(len(urls)))
        for url in urls:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as f: #nosec
                log.info(f"downloading pdf: {url}")
                pdf_content = f.read()
                with open(url.split("/")[-1], "wb") as f_writer:
                    f_writer.write(pdf_content)
        now = datetime.now()
        time_taken = now - then
        ocp.set_measurement("download_brochure", int(time_taken.total_seconds()))
        

    @staticmethod
    async def run(url, ocp):
        log.info(f"starting traffic on : {url}")
        browser_path = os.getenv("EXECUTABLE_PATH", None)
        browser = await launch(executablePath=browser_path, 
                              args=[
            '--no-sandbox',
            '--disable-dev-shm-usage'])
        page = await browser.newPage()
        actions = ["home_page", "download_brochure"]
        for action in actions:
            m = getattr(TrafficGenerator, action)
            await m(page, url, ocp)
        await browser.close()
