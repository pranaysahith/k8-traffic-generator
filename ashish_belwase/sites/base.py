import logging

log = logging.getLogger("GW:traffic_g")


class BaseSite:
    """
        Base Class to handle automation of site.
        It contains common methods used for site automations.
        All new sites will inherit from this class
    """

    Allowed_Methods = ["open", "follow", "download", "upload"]

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
