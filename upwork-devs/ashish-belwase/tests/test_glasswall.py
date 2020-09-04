from unittest import TestCase
from pyppeteer import launch
from syncer import sync

from sites.glasswall import Glasswallsolutions


class TestGlassWall(TestCase):
    def setUp(self):
        self.browser = sync(launch(args=['--no-sandbox']))
        self.url = "https://glasswallsolutions.com"

    def tearDown(self):
        sync(self.browser.close())

    # @sync
    # async def test_download(self):
    #     page = await self.browser.newPage()
    #     pdfs = await Glasswallsolutions.download(page, self.url)
    #     self.assertEqual(len(pdfs), 3)
    #     for pdf in pdfs:
    #         with self.subTest(pdf=pdf):
    #             self.assertTrue(".pdf" in pdf)

    @sync
    async def test_products(self):
        page = await self.browser.newPage()
        products = await Glasswallsolutions.products(page, self.url)
        self.assertEqual(len(products), 7)

    @sync
    async def test_pricing(self):
        page = await self.browser.newPage()
        products = await Glasswallsolutions.pricing(page, self.url)
        self.assertEqual(len(products), 3)
