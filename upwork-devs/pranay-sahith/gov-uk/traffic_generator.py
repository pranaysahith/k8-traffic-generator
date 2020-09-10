from pyppeteer import launch
import os
import time
import asyncio
import logging

log = logging.getLogger("TG:gov_uk")


class TrafficGenerator():

    def __init__(self, url):
        super().__init__()
        self.url = url

    async def run(self):
        browser_path = os.getenv("EXECUTABLE_PATH", None)
        self.browser = await launch(headless=True, executablePath=browser_path, 
                            args=[
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--ignore-certificate-errors',
            '--enable-features=NetworkService'])
        self.page = await self.browser.newPage()
        await self.download_files("pdf")

    async def download_files(self, search_by='pdf'):
        log.info(f"searching for keyword: {search_by}")
        await self.page.goto(self.url)
        await self.page.type("input", search_by)
        await self.page.keyboard.press("Enter")

        
        href_list = await self.page.xpath("//li[@class='gem-c-document-list__item  ']/a")
        log.info(f"found {len(href_list)} number of search results")
        urls_list = []
        for att in href_list:
            url = await self.page.evaluate(
                            '(att) => att.href',
                            att
                )
            urls_list.append(url)

        for u in urls_list[0:5]:
            try:
                log.info(f"opening {u}")
                await self.page.goto(u, waitUntil="networkidle0")
                time.sleep(3)
                download_urls = await self.page.xpath("//a[contains(@href, '.pdf')]")
                log.info(f"number of files found: {len(download_urls)}")
                time.sleep(3)
                for dl_url in download_urls:
                    await dl_url.click()
            #         print(page.url)
                    break

                time.sleep(3)
            except Exception as e:
                log.error(e)
        await self.browser.close()
