from pyppeteer import launch
import os
import time
import asyncio
import logging

class FileDrop():

    def __init__(self, url):
        super().__init__()
        self.url = url

    async def start(self, headless):
        browser_path = os.getenv("EXECUTABLE_PATH", None)
        self.browser = await launch(headless=headless, executablePath=browser_path, 
                            args=[
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--ignore-certificate-errors',
            '--enable-features=NetworkService'])
        self.page = (await self.browser.pages())[0]
        self.page.setDefaultNavigationTimeout(300000)

    async def is_clean_file(self, local_file_name):
        await self.page.goto(self.url)
        upload_element = await self.page.xpath("//input[@type='file']")
        await upload_element[0].uploadFile(local_file_name)
        await self.page.waitForXPath("//a[@href='#analysis']")
        results_elements = await self.page.xpath("//a[@href='#analysis']")
        await results_elements[0].click()
        time.sleep(3)
        clean_element = await self.page.xpath("//div[@class='section-title clean-title']")
        if len(clean_element) < 1:
            return None
        else:
            clean_element = clean_element[0]
            text = await self.page.evaluate(
                                '(clean_element) => clean_element.textContent',
                                clean_element
                    )
            return text

    async def close_browser(self):
        await self.browser.close()
