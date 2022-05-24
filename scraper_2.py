import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlencode
from urllib.parse import urlparse
import concurrent.futures
import csv
import pandas as pd

from utils import csv_reader, csv_writer

API_KEY = "38212cb84176f162872cd422ddd5a50b"
NUM_RETRIES = 3
NUM_THREADS = 16

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
list_of_urls = []


def get_scraperapi_url(url):
    payload = {
        "api_key": API_KEY,
        "url": url,
        "country_code": "au",
        "keep_headers": "true",
    }
    proxy_url = "http://api.scraperapi.com/?" + urlencode(payload)
    return proxy_url


def fetch_ads(url):
    keywords = csv_reader()
    for keyword in keywords:
        initial_params["q"] = keyword
        for page in range(0, 4):
            params = pagination_params

            params["start"] = str(page * 60)

            params["q"] = keyword
            url_str = base_url + urlencode(params)
            list_of_urls.append(url_str)

            for _ in range(NUM_RETRIES):
                try:
                    response = requests.get(get_scraperapi_url(url), headers=headers)
                    if response.status_code in [200, 404]:
                        break
                except requests.exceptions.ConnectionError:
                    response = ""
                if response.status_code == 200:
                    ad_urls = []
                    content = BeautifulSoup(response.text, "lxml")

                    for ad in content.find_all("a", {"class": "sh-np__click-target"}):
                        try:
                            r = requests.get(
                                "https://www.google.com" + ad["href"], headers=headers
                            )
                            g_ad_url = r.url
                            ad_urls.append(urlparse(g_ad_url).netloc)
                            print(urlparse(g_ad_url).netloc)
                        except:
                            pass

                    for idx in range(len(ad_urls)):

                        results.append({"Ad_Url": ad_urls[idx]})


with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    executor.map(fetch_ads, list_of_urls)

print(results)

# try:
#     with open("temp_data.csv", mode="w", encoding="utf-8", newline="") as file:
#         writer = csv.DictWriter(file, fieldnames=results[0].keys())
#         writer.writeheader()

#         for row in results:
#             writer.writerow(row)
# except:
#     pass
# try:
#     df = pd.read_csv("temp_data.csv")
#     df.drop_duplicates(inplace=True)
#     df.to_csv("clean_file.csv", index=False)
# except:
#     pass
