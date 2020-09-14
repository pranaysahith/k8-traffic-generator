import logging
from pyppeteer import launch
from sites import *
from helper import Helper

log = logging.getLogger("GW:traffic_g")


class TrafficGenerator:
    @staticmethod
    def get_site(url):
        site = BaseSite
        domain = Helper.get_domain_from_url(url)
        try:
            site = globals()[domain.title()]()
        except:
            pass
        return site

    @staticmethod
    async def run(url, action):
        site = TrafficGenerator.get_site(url)
        if action:
            if action not in site.Allowed_Methods:
                log.info(f"Invalid action `{action}` on `{site.__name__}`")
                return
        else:
            action = site.get_rand_action()

        log.info(f"starting traffic on : {url} , action : {action}")

        browser = await launch(args=["--no-sandbox"])
        page = await browser.newPage()
        m = getattr(site, action)
        await m(page, url)
        await browser.close()
