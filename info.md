https://www.google.com/search?safe=active&sxsrf=ALeKk00d7WrRTMvmhypG20E5MOEWpRwKlw%3A1601591747498&ei=w1l2X52DHoPatAXElILQDg&q=lift+installation&oq=nasd&gs_lcp=CgZwc3ktYWIQAxgAMgwIIxAnEJ0CEEYQ-gEyBAgjECcyBAgjECcyCggAELEDEIMBEEMyCggAELEDEIMBEEMyCAgAELEDEIMBMgcIABCxAxBDMgcIABCxAxBDMgcIABCxAxBDMgoIABCxAxCDARBDOgQIABBHOgUIABCxAzoHCCMQ6gIQJzoHCCMQJxCdAjoECAAQQ1DszQ5Y9tkOYPjkDmgBcAJ4BYABqQOIAZ4NkgEJMS43LjEuMC4xmAEAoAEBqgEHZ3dzLXdperABCsgBCMABAQ&sclient=psy-ab

https://www.google.com/search?q=lift+installation&sxsrf=ALiCzsYBgwb-aQaIzX0gteW_dfb3Ae0ejg:1652897395525&source=lnms&tbm=shop&sa=X&ved=2ahUKEwii2fDQ0un3AhVjmuYKHRFvDikQ_AUoA3oECAEQBQ&biw=962&bih=625&dpr=1

url = 'https://www.google.com/search?q=lift+installation&sxsrf=ALiCzsYBgwb-aQaIzX0gteW_dfb3Ae0ejg:1652897395525&source=lnms&tbm=shop&sa=X&ved=2ahUKEwii2fDQ0un3AhVjmuYKHRFvDikQ_AUoA3oECAEQBQ&biw=962&bih=625&dpr=1'


headers = {
    'authority': 'www.google.com',
    'sec-ch-dpr': '1',
    'sec-ch-viewport-width': '1366',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Yandex";v="22"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-full-version': '"22.3.3.886"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-platform': '"Linux"',
    'sec-ch-ua-platform-version': '"5.4.0"',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version-list': '" Not A;Brand";v="99.0.0.0", "Chromium";v="98.0.4758.886", "Yandex";v="22.3.3.886"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.google.com/',
    'accept-language': 'en,ru;q=0.9',
    }

_headers = [(k, v) for k, v in headers.items()]

base_url = 'https://www.google.com/search?'


pagination_params = {
    'q': 'lift installation',
	'source': 'lnms',
    'tbm': 'shop',
    'ei': 'aW-HYv74MrCOseMP_8OumAY',
    'start': '10',
    'sa': 'X',
    'ved': '0ahUKEwikobSm8e33AhUjUGwGHQVfDr84PBDy0wMIpw0',
    'biw': '480',
    'bih': '665',
    'dpr': '1',
    }

params = {
    'q': 'lift installation',
	'source': 'lnms',
    'tbm': 'shop',
    'sa': 'X',
    'ved': '0ahUKEwikobSm8e33AhUjUGwGHQVfDr84PBDy0wMIpw0',
    'biw': '480',
    'bih': '665',
    'dpr': '1',
    }

initial_params = {
    "q": "lift installation",
    "sxsrf": "ALiCzsYBgwb-aQaIzX0gteW_dfb3Ae0ejg:1652897395525",
    "source": "lnms",
    "tbm": "shop",
    "sa": "X",
    "ved": "2ahUKEwii2fDQ0un3AhVjmuYKHRFvDikQ_AUoA3oECAEQBQ",
    "biw": "962",
    "bih": "625",
    "dpr": "1",
}

pagination_params = {
    "q": "lift installation",
    "sxsrf": "ALiCzsYBgwb-aQaIzX0gteW_dfb3Ae0ejg:1652897395525",
    "source": "lnms",
    "tbm": "shop",
    "sa": "X",
    "ved": "2ahUKEwii2fDQ0un3AhVjmuYKHRFvDikQ_AUoA3oECAEQBQ",
    "biw": "962",
    "bih": "625",
    "dpr": "1",
}

url = base_url + urllib.parse.urlencode(params)

import urllib.request
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler(
            {'http': 'http://lum-customer-c_4ae025b1-zone-data_center-country-au:15kcfdu564mt@zproxy.lum-superproxy.io:22225',
            'https': 'http://lum-customer-c_4ae025b1-zone-data_center-country-au:15kcfdu564mt@zproxy.lum-superproxy.io:22225'}))

opener.addheaders = _headers

data = opener.open(url)

data.read()

content = BeautifulSoup(data.read(), 'lxml')
ads_list = content.find_all('a', {'class': 'sh-np__click-target'})
for ad in ads_list:
print('https://www.google.com' + ad['href'])

def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'country_code': 'au', 'keep_headers': 'true'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

r = requests.get(get_scraperapi_url(url), headers=headers)

ad_urls = ['https://www.google.com' + ad['href'] for ad in content.find_all('a', {'class':'sh-np__click-target'})]
title = [t.text for t in content.find_all('div', {'class':'sh-np__product-title translate-content'})]