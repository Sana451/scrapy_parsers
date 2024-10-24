import pandas
import requests
from bs4 import BeautifulSoup

cookies = {
    'session-2': 'uc07cqujmqdci77h2rskb340lu',
    'allowCookie': '1',
    'cookiePreferences': '{"groups":{"technical":{"name":"technical","cookies":{"allowCookie":{"name":"allowCookie","active":true},"cookieDeclined":{"name":"cookieDeclined","active":true},"csrf_token":{"name":"csrf_token","active":true},"cookiePreferences":{"name":"cookiePreferences","active":true},"currency":{"name":"currency","active":true},"slt":{"name":"slt","active":true},"nocache":{"name":"nocache","active":true},"x-cache-context-hash":{"name":"x-cache-context-hash","active":true},"paypal-cookies":{"name":"paypal-cookies","active":true},"shop":{"name":"shop","active":true},"session":{"name":"session","active":true}},"active":true},"comfort":{"name":"comfort","cookies":{"sUniqueID":{"name":"sUniqueID","active":true}},"active":false},"statistics":{"name":"statistics","cookies":{"partner":{"name":"partner","active":true},"wbm_tag_manager":{"name":"wbm_tag_manager","active":true},"x-ua-device":{"name":"x-ua-device","active":true}},"active":false}},"hash":"WyJhbGxvd0Nvb2tpZSIsImNvbWZvcnQiLCJjb29raWVEZWNsaW5lZCIsImNvb2tpZVByZWZlcmVuY2VzIiwiY3NyZl90b2tlbiIsImN1cnJlbmN5Iiwibm9jYWNoZSIsInBhcnRuZXIiLCJwYXlwYWwtY29va2llcyIsInNVbmlxdWVJRCIsInNlc3Npb24iLCJzaG9wIiwic2x0Iiwic3RhdGlzdGljcyIsInRlY2huaWNhbCIsIndibV90YWdfbWFuYWdlciIsIngtY2FjaGUtY29udGV4dC1oYXNoIiwieC11YS1kZXZpY2UiXQ=="}',
    'QEtRRWsNaGiCWKeD9M_Haris6Ho': 'KAjiSenxyAM9B90fok66Uv92y4s',
    'QEtRRWsNaGiCWKeD9M_Haris6Ho': 'KAjiSenxyAM9B90fok66Uv92y4s',
    'PiNItIMBs1PkgwNz_RpGEi9Icu4': '1728969470',
    'KUzx7IaDJL86Q4LxSIUAHx7gfuc': '1729055870',
    '--cv2u0HKbO9KRsgG1zDykal4mI': 'pfP85Hpgv4xDLPxYC7tofxfUkUY',
    '__csrf_token-2': 'Z8cMYbYhYnSkiBpUyAfafMUzwH2BOx',
    'session-1': 'ao4p6urahnm3a36p4i2tde777j',
    '__csrf_token-1': 'ubrFnga11Nr2oeEnJIIKceHCQ61ra3',
    'shop': '2',
    'currency': '1',
    '__hstc': '9267242.75d0249612114fbb19382a1e0ef233ce.1728971805584.1728971805584.1728971805584.1',
    'hubspotutk': '75d0249612114fbb19382a1e0ef233ce',
    '__hssrc': '1',
    '__hssc': '9267242.1.1728971805585',
    'x-ua-device': 'tablet',
}

all_links = set()

for i in range(1, 22):
    params = {'p': i, }
    response = requests.get('https://www.twk.de/en/products/',
                            params=params,
                            cookies=cookies,
                            )
    soup = BeautifulSoup(response.content, "html.parser")
    links = [a["href"] for a in soup.select("a.product--title")]
    print(f"Page {i}")
    print(f"links found: {len(links)}")
    all_links.update(links)

pandas.DataFrame(all_links).to_csv(
    "/twk_de/twk_de/results/twk.de.links3.csv", index=False)
