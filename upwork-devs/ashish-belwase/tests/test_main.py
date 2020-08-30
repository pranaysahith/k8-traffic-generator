from unittest import TestCase
from unittest.mock import patch
from pyppeteer import launch
from syncer import sync
import sys

from main import Main


class TestMain(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_command_line_args(self):
        action = "open"
        url = "https://glasswallsolutions.com"
        testargs = ["python", "-u", url, "-a", action]
        with patch.object(sys, "argv", testargs):
            args = Main.get_command_line_args()
            self.assertEqual(args.action, action)
            self.assertEqual(args.url, url)
