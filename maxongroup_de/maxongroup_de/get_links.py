import re

import pandas
from bs4 import BeautifulSoup

import requests

DOMAIN = "https://www.maxongroup.de"

cookies = {
    'JSESSIONID': 'Y2-2062f923-6441-466d-8603-ad8e2d7b90c3.node3',
    'TS01c7a627': '01245915d7fb980b837dd4223549ea1d2a955f6ef29aa96f0338b074563831dedd3f098bd3c0be989f77c0aa8784ccaf4e211cf91af4408fb491ab2e19c590d013ba8687cb',
    '_gcl_au': '1.1.901293010.1728657623',
    '_ga': 'GA1.2.1595138255.1728657624',
    '_gid': 'GA1.2.1699274773.1728657624',
    'isSdEnabled': 'true',
    'hubspotutk': '11228325cf7623f9cb12bf87e47727a8',
    '__hssrc': '1',
    '_et_coid': '90733702604c03e769b992d4869c3531',
    '__hstc': '227576258.11228325cf7623f9cb12bf87e47727a8.1728657624227.1728657624227.1728662066119.2',
    'RT': '"z=1&dm=maxongroup.de&si=mowe6b7g6sg&ss=m24u44wt&sl=0&tt=0"',
    '__hssc': '227576258.4.1728662066119',
    'TS01a5dca8': '01245915d7cc760731b7e4b136ebab844771f1e26eb4f94930a61bf7dd7bc2941bb511a2e8ef1db55a9a896d8c19e11c543c9bfaa3',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=Y2-2062f923-6441-466d-8603-ad8e2d7b90c3.node3; TS01c7a627=01245915d7fb980b837dd4223549ea1d2a955f6ef29aa96f0338b074563831dedd3f098bd3c0be989f77c0aa8784ccaf4e211cf91af4408fb491ab2e19c590d013ba8687cb; _gcl_au=1.1.901293010.1728657623; _ga=GA1.2.1595138255.1728657624; _gid=GA1.2.1699274773.1728657624; isSdEnabled=true; hubspotutk=11228325cf7623f9cb12bf87e47727a8; __hssrc=1; _et_coid=90733702604c03e769b992d4869c3531; __hstc=227576258.11228325cf7623f9cb12bf87e47727a8.1728657624227.1728657624227.1728662066119.2; RT="z=1&dm=maxongroup.de&si=mowe6b7g6sg&ss=m24u44wt&sl=0&tt=0"; __hssc=227576258.4.1728662066119; TS01a5dca8=01245915d7cc760731b7e4b136ebab844771f1e26eb4f94930a61bf7dd7bc2941bb511a2e8ef1db55a9a896d8c19e11c543c9bfaa3',
    'Pragma': 'no-cache',
    'Referer': 'https://www.maxongroup.de/maxon/view/category',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

categories = [
    "https://www.maxongroup.de/maxon/view/category/Compact-Drive",
    "https://www.maxongroup.de/maxon/view/category/motor",
    "https://www.maxongroup.de/maxon/view/category/gear",
    "https://www.maxongroup.de/maxon/view/category/control",
    "https://www.maxongroup.de/maxon/view/category/sensor",
    "https://www.maxongroup.de/maxon/view/category/accessory"
]

STOP_PHRASE = "Leider keine Treffer"

all_urls = []

for cat in categories:
    page_num = 1

    while True:
        params = {'pn_id': 'ProductSearch', 'pn_p': page_num, 'pn_ok': '', '_': '1728662092423'}
        url = cat.split("/")
        url.insert(-1, "prodfilter")
        url = "/".join(url)

        response = requests.get(
            url=url,
            params=params,
            cookies=cookies,
            headers=headers,
        )

        if STOP_PHRASE in response.text:
            break

        soup = BeautifulSoup(response.content, "html.parser")
        pattern = re.compile("data-detailUrl=\"(.+)\"")
        relative_urls = re.findall(pattern, response.text)
        prod_urls = [DOMAIN + url for url in relative_urls]
        print(f"page_num: {page_num} found", len(prod_urls), f"(Category: {cat})")
        all_urls.extend(prod_urls)

        page_num += 1

    print("All prod urls count: ", len(all_urls))

pandas.DataFrame(all_urls, columns=["url"]).to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/maxongroup_de/maxongroup_de/results/maxogroup.de.links.csv",
    index=False)
