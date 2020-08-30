from urllib.parse import urlparse
import urllib.request
from datetime import datetime
import os


class Helper:
    @staticmethod
    def get_domain_from_url(url):
        parsed_uri = urlparse(url)
        domain = "{uri.netloc}".format(uri=parsed_uri)
        return domain

    @staticmethod
    def get_file_from_url(url):
        DIR = "temp"
        d = str(datetime.now())
        d = DIR + "/" + "_".join(d.split(" "))
        if not os.path.exists(DIR):
            os.makedirs(DIR)
        urllib.request.urlretrieve(url, d)
