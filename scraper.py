import httpx
import asyncio
from bs4 import BeautifulSoup
from decouple import config
from urllib.parse import urlencode
from urllib.parse import urlparse
import os

from utils import csv_reader, csv_writer

SCRAPERAPI_KEY = config("API_KEY")
NUM_RETRIES = 3


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


def get_scraperapi_url(url):
    payload = {
        "api_key": SCRAPERAPI_KEY,
        "url": url,
        "country_code": "au",
        "keep_headers": "true",
    }
    proxy_url = "http://api.scraperapi.com/?" + urlencode(payload)
    return proxy_url


async def log_request(request):
    print(f"Request: {request.method} {request.url}")


async def log_response(response):
    request = response.request
    print(f"Response: {request.method} {request.url} - Status: {response.status_code}")


async def fetch_pages(keyword, page_no):
    initial_params["q"] = keyword
    if not page_no:
        params = initial_params
        url = base_url + urlencode(params)
    else:
        params = pagination_params

        params["start"] = str(page_no * 60)

        params["q"] = keyword
        url = base_url + urlencode(params)

    async with httpx.AsyncClient(
        event_hooks={"request": [log_request], "response": [log_response]}
    ) as client:
        response = await client.get(
            get_scraperapi_url(url), headers=headers, timeout=None
        )

        return response


async def parse_page(html):

    ad_urls = []
    content = BeautifulSoup(html, "lxml")

    for ad in content.find_all("a", {"class": "sh-np__click-target"}):
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    "https://www.google.com" + ad["href"], headers=headers, timeout=None
                )
                url = str(r.url)
                ad_urls.append(urlparse(url).netloc)
                print(urlparse(url).netloc)
        except:
            pass

    for idx in range(len(ad_urls)):

        results.append({"Ad_Url": ad_urls[idx]})

    return results


async def run_scraper(file_path):
    tasks = []
    kw = await csv_reader(file_path)
    for k in kw:
        for page in range(0, 4):
            for _ in range(NUM_RETRIES):
                try:
                    response = await fetch_pages(k, page)
                    if response.status_code in [200, 404]:
                        break
                except httpx.ConnectError:
                    response = ""
            if response.status_code == 200:
                tasks.append(asyncio.create_task(parse_page(response.content)))

    ad_data = await asyncio.gather(*tasks)

    await csv_writer(ad_data[0])

    return ad_data


if __name__ == "__main__":
    file_path = os.path.abspath("keywords_for_scraper.csv")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_scraper(file_path))
