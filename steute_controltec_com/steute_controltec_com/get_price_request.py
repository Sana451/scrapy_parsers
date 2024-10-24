import requests
from bs4 import BeautifulSoup

import requests

cookies = {
    'fe_typo_user': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiYmI5ZjM4ODI5OWNlOTQyNDBkZDZkN2NmZmUwZTU2YzciLCJ0aW1lIjoiMjAyNC0xMC0xOVQxMzo1MToyNiswMjowMCIsInNjb3BlIjp7ImRvbWFpbiI6Ind3dy5zdGV1dGUtY29udHJvbHRlYy5jb20iLCJob3N0T25seSI6dHJ1ZSwicGF0aCI6Ii8ifX0.ySomuOqh6Zx2-vv2fFxlx8C4uTRGVlDlWjcn413LMu8',
    'staticfilecache': 'typo_user_logged_in',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7',
    'cache-control': 'no-cache',
    # 'cookie': 'fe_typo_user=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiYmI5ZjM4ODI5OWNlOTQyNDBkZDZkN2NmZmUwZTU2YzciLCJ0aW1lIjoiMjAyNC0xMC0xOVQxMzo1MToyNiswMjowMCIsInNjb3BlIjp7ImRvbWFpbiI6Ind3dy5zdGV1dGUtY29udHJvbHRlYy5jb20iLCJob3N0T25seSI6dHJ1ZSwicGF0aCI6Ii8ifX0.ySomuOqh6Zx2-vv2fFxlx8C4uTRGVlDlWjcn413LMu8; staticfilecache=typo_user_logged_in',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.steute-controltec.com/de/produkt/gf-2-1s-1s-hid-5m-100111',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

params = {
    'tx_ofweco_pricerequest[action]': 'priceRequest',
    'tx_ofweco_pricerequest[article]': '48894',
    'tx_ofweco_pricerequest[controller]': 'Weco',
    'cHash': 'fad1024d492333b28ca3fb8b5060e8c7',
}

response = requests.get(
    'https://www.steute-controltec.com/de/produkt/weco/pricerequest',
    params=params,
    cookies=cookies,
    headers=headers,
)


# soup = BeautifulSoup(response.json()["view"], "html.parser")
# price = soup.select(".product__price__number")
# price = price[0].text.strip().replace(" €", "")

# print(price)

print(response)