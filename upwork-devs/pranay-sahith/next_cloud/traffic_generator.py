import logging
import urllib.request
from datetime import datetime
import os
import asyncio
from pyppeteer import launch
from urllib.parse import quote
import time

loop = asyncio.get_event_loop()
log = logging.getLogger("GW:traffic_g")


class TrafficGenerator:

    def __init__(self, url, ocp, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self.url = url
        self.ocp = ocp

    async def launch_browser(self):
        browser_path = os.getenv("EXECUTABLE_PATH", None)
        browser = await launch(headless=True, executablePath=browser_path, 
                              args=[
            '--no-sandbox',
            '--disable-dev-shm-usage'])
        self.page = await browser.newPage()
        # await self.page.setCacheEnabled(False)

    async def go_home(self):
        log.info(f"opening url: {self.url}")
        await self.page.goto(self.url)

    async def login(self):
        # login
        log.info("login to nextlcloud")
        await self.page.type("input", self.username)
        await self.page.keyboard.press("Tab")
        await self.page.type("input", self.password)
        await self.page.keyboard.press('Enter')
        await self.page.waitForNavigation()

    async def download_file(self, remote_file_path):
        # download file
        has_dir = True if len(remote_file_path.split('/')) > 2 else False
        if has_dir:
            dir_name = remote_file_path.split("/")[1]
            print(f"traversing into dir: {dir_name}")
            dir_elements = await self.page.xpath(f"//td//span[@class='innernametext' and text()='{dir_name}']")
            await dir_elements[0].click()
            await self.download_file("/" + "/".join(remote_file_path.split("/")[2:]))
        else:
            time.sleep(2)
            file_name = remote_file_path.split("/")[-1]
            file_element = await self.page.xpath(f"//a[@class='name' and contains(@href,'{file_name}')]/span/a[@class='action action-menu permanent']")
            await file_element[0].click()
            print(f"downloading file: {file_name}")
            download_elements = await self.page.xpath("//li[@class=' action-download-container']/a[@class='menuitem action action-download permanent' and @data-action='Download']")
            await download_elements[0].click()

    async def create_dir(self, new_dir_name):
        new_dir_name = new_dir_name.strip("/")
        time.sleep(2)
        print(f"creating dir: {new_dir_name}")
        await self.page.click("span.icon.icon-add")
        await self.page.click("a.menuitem")
        elements = await self.page.xpath("//input[@value='New folder']")
        element = elements[0]
        await element.type(new_dir_name)
        await self.page.keyboard.press('Enter')
        time.sleep(2)

    async def open_dir(self, dir_name):
        # open dir
        print(f"opening dir: {dir_name}")
        dir_elements = await self.page.xpath(f"//td//span[@class='innernametext' and text()='{dir_name}']")
        await dir_elements[0].click()


    async def upload_file(self, local_file_name):
        # upload
        print(f"uploading file: {local_file_name}")
        upload_element = await self.page.xpath("//input[@type='file']")
        await upload_element[0].uploadFile(local_file_name)


    async def run(self):
        log.info(f"starting traffic on : {self.url}")
        files = ["/Photos/Coast.jpg", "/Nextcloud intro.mp4", "/Documents/About.txt"]
        await self.launch_browser()
        await self.go_home()
        await self.login()
        time.sleep(5)
        # for f in files:
        #     await self.download_file(quote(f))
        #     # await self.go_home()
        #     print(f"goto {self.url}")
        #     await self.page.setCacheEnabled(False)
        #     response = await self.page.goto(self.url, waitUntil="networkidle0")
        #     if response is None:
        #         await self.page.waitForResponse(self.url)
            # await self.page.waitForNavigation()
        user = "user_a"
        remote_dir = "/target_dir" + "_" + user
        # await self.go_home()
        # await self.create_dir(remote_dir)
        
        upload_files = [f.split("/")[-1] for f in files]
        for dir_name in remote_dir.split("/")[1:]:
            await self.open_dir(dir_name)
        
        for f in upload_files:
            await self.upload_file(f)
            # os.remove(f)
