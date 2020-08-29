import logging
from pyquery import PyQuery as pq

log = logging.getLogger("GW:traffic_g")


class BaseSite:
    """
        Base Class to handle automation of site.
        It contains common methods used for site automations.
        All new sites will inherit from this class
    """

    Allowed_Methods = ["open", "follow", "download", "upload"]
    DEFAULT_PAGE_WAIT = 4000

    @staticmethod
    async def get_page(page, url):
        await page.goto(url)
        doc = pq(await page.content())
        return doc

    @staticmethod
    async def wait_for_element(element, MAX_ATTEMPT=10):
        is_visible = False
        attempt = 0
        while is_visible == False:
            await element._scrollIntoViewIfNeeded()
            is_visible = await element.isIntersectingViewport()
            attempt += 1
            if attempt > MAX_ATTEMPT and not is_visible:
                break
        return is_visible

    @staticmethod
    async def open(page, url):
        await page.goto(url)
        log.info(f"loaded url : {url}")

    @staticmethod
    async def follow(page, url):
        pass

    @staticmethod
    async def upload(page, url, data={}):
        pass
