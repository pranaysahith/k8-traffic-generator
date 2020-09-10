from pyppeteer import launch
import requests
import os
import time
import logging
import sys

log = logging.getLogger("TG:gov_uk")
log.setLevel(logging.INFO)
logging.basicConfig( stream=sys.stdout )


class TrafficGenerator():

    def __init__(self, url):
        super().__init__()
        self.url = url
        requests.packages.urllib3.disable_warnings()

    async def run(self, num_files):
        browser_path = os.getenv("EXECUTABLE_PATH", None)
        self.browser = await launch(headless=True, executablePath=browser_path,
                            args=[
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--ignore-certificate-errors',
            '--enable-features=NetworkService'])
        self.page = (await self.browser.pages())[0]
        self.page.setDefaultNavigationTimeout(600000)
        await self.download_files("pdf", num_files)

    async def download_files(self, search_by='pdf', num_files=10):
        log.info(f"searching for keyword: {search_by}")
        await self.page.goto(self.url)
        await self.page.type("input", search_by)
        await self.page.keyboard.press("Enter")

        await self.page.waitForXPath("//li[@class='gem-c-document-list__item  ']/a")
        href_list = await self.page.xpath("//li[@class='gem-c-document-list__item  ']/a")
        log.info(f"found {len(href_list)} search results")
        urls_list = []
        for att in href_list:
            url = await self.page.evaluate(
                            '(att) => att.href',
                            att
                )
            urls_list.append(url)

        saved_files = 0
        for u in urls_list:
            try:
                if saved_files >= num_files:
                    break
                log.info(f"opening {u}")
                await self.page.goto(u, waitUntil="networkidle0")
                time.sleep(3)
                download_urls = await self.page.xpath("//a[contains(@href, '.pdf')]")
                log.info(f"number of files found: {len(download_urls)}")
                time.sleep(3)
                for dl_url in download_urls:
                    file_url = await self.page.evaluate(
                    '(dl_url) => dl_url.href',
                    dl_url
                    )
                    if "glasswall" not in file_url:
                        continue
                    self.save_file(file_url)
                    saved_files += 1
                    if saved_files >= num_files:
                        break

                time.sleep(3)
            except Exception as e:
                log.error(e)
        await self.browser.close()

    def save_file(self, file_url):
        try:
            log.info(f"saving file {file_url}")
            res = requests.get(file_url, verify=False)
            with open(file_url.split("/")[-1], "wb") as f:
                f.write(res.content)
        except Exception as e:
            log.error(e)
