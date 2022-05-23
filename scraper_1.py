import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlencode
from urllib.parse import urlparse
import re
import os

from utils import csv_reader, csv_writer

API_KEY = "38212cb84176f162872cd422ddd5a50b"
NUM_RETRIES = 3


def get_scraperapi_url(url):
    payload = {
        "api_key": API_KEY,
        "url": url,
        "country_code": "au",
        "keep_headers": "true",
    }
    proxy_url = "http://api.scraperapi.com/?" + urlencode(payload)
    return proxy_url


class GoogleAdUrlScraper:
    def __init__(self, filepath, **kargs):
        self.file_path = filepath

    base_url = "https://www.google.com/search?"

    headers = {
        "authority": "www.google.com",
        "sec-ch-dpr": "1",
        "sec-ch-viewport-width": "1366",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Yandex";v="22"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-full-version": '"22.3.3.886"',
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-platform": '"Linux"',
        "sec-ch-ua-platform-version": '"5.4.0"',
        "sec-ch-ua-model": '""',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version-list": '" Not A;Brand";v="99.0.0.0", "Chromium";v="98.0.4758.886", "Yandex";v="22.3.3.886"',
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": "https://www.google.com/",
        "accept-language": "en,ru;q=0.9",
    }

    pagination_params = {
        "q": "lift installation",
        "source": "lnms",
        "tbm": "shop",
        "ei": "aW-HYv74MrCOseMP_8OumAY",
        "start": "",
        "sa": "X",
        "ved": "0ahUKEwikobSm8e33AhUjUGwGHQVfDr84PBDy0wMIpw0",
        "biw": "480",
        "bih": "665",
        "dpr": "1",
    }

    initial_params = {
        "q": "",
        "source": "lnms",
        "tbm": "shop",
        "sa": "X",
        "ved": "0ahUKEwikobSm8e33AhUjUGwGHQVfDr84PBDy0wMIpw0",
        "biw": "480",
        "bih": "665",
        "dpr": "1",
    }

    results = []

    def fetch(self, keyword, page):
        self.initial_params["q"] = keyword

        if not page:
            params = self.initial_params
            url = self.base_url + urlencode(params)
        else:
            params = self.pagination_params

            params["start"] = str(page * 60)

            params["q"] = keyword
            url = self.base_url + urlencode(params)

        response = requests.get(get_scraperapi_url(url), headers=self.headers)
        print(
            "HTTP GET request to URL: %s | Status code: %s"
            % (response.url, response.status_code)
        )

        return response

    def parse(self, html):

        ad_urls = []
        content = BeautifulSoup(html, "lxml")

        for ad in content.find_all("a", {"class": "sh-np__click-target"}):
            print("https://www.google.com" + ad["href"])
            try:
                r = requests.get(
                    "https://www.google.com" + ad["href"],
                    headers=self.headers,
                )
                url = r.url
                ad_urls.append(urlparse(url).netloc)
            except:
                pass
        print(len(ad_urls))

        for idx in range(len(ad_urls)):
            try:
                ad_link = ad_urls[idx]
            except:
                ad_link = ""

            self.results.append({"Ad_Url": ad_link})

        return self.results

    def run(self):
        kw = csv_reader(self.file_path)
        for k in kw:
            for page in range(0, 4):
                for _ in range(NUM_RETRIES):
                    try:
                        response = self.fetch(k, page)
                        if response.status_code in [200, 404]:
                            break
                    except requests.exceptions.ConnectionError:
                        response = ""
                if response.status_code == 200:
                    ad_data = self.parse(response.text)
                time.sleep(5)

                csv_writer(ad_data)

        return ad_data


if __name__ == "__main__":
    file_path = os.path.abspath("keywords_for_scraper.csv")
    scraper = GoogleAdUrlScraper(file_path)
    data = scraper.run()
    csv_writer(data)
