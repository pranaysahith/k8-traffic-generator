import logging
from pyquery import PyQuery as pq

from helper import Helper
from .base import BaseSite

log = logging.getLogger("GW:traffic_g")


class Glasswallsolutions(BaseSite):

    @staticmethod
    async def download_pdf(page, url):
        await page.goto(url)
        doc = pq(await page.content())
        pdfs = doc.find('a[href*=".pdf"]')
        log.info("downloading {} pdfs".format(len(pdfs)))
        for pdf in pdfs:
            url = pdf.get("href")
            Helper.get_file_from_url(url)

    
    @staticmethod
    async def download(page, url):
        await Glasswallsolutions.download_pdf(page, url)
