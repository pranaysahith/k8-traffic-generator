import logging
from pyppeteer import launch
from sites.base import BaseSite
from sites.glasswall import Glasswallsolutions
from helper import Helper

log = logging.getLogger("GW:traffic_g")


class TrafficGenerator:

    Allowed_Sites = {"glasswallsolutions.com": Glasswallsolutions}

    @staticmethod
    def get_site(url):
        domain = Helper.get_domain_from_url(url)
        site = TrafficGenerator.Allowed_Sites.get(domain, None)
        return site

    @staticmethod
    async def run(url, action):
        site = TrafficGenerator.get_site(url)
        if not site:
            log.info("requested url is not a registered site")
            return

        if action:
            if action not in site.Allowed_Methods:
                log.info(f"Invalid action `{action}` on `{site.__name__}`")
                return
        else:
            action = site.get_rand_action()

        log.info(f"starting traffic on : {url} , action : {action}")

        browser = await launch()
        page = await browser.newPage()
        m = getattr(site, action)
        await m(page, url)
        await browser.close()
