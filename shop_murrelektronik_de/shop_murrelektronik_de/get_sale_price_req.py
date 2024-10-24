import json

import requests



cookies = {
    'sid_key': 'oxid',
    'visitor_id883653': '892544652',
    'visitor_id883653-hash': '5754bdd2b4eab77d9963edf2fc0056f55a4e6c146955a24c7a567f585f6e82b7dbb92532fabd963e33fce58d72357b1464c44794',
    'showlinksonce': '1',
    'oxid_1_autologin': '1',
    'oxid_1': 'osl%40famaga.de%40%40%40%242y%2410%24dZo31hQK8PfmnWXz13nkhOUZbuSVgWnKYiF3duGW4S9PXFE2JhlJ.',
    'sid': 'pars0ihmvi1467lbins9nl7ptq',
    'language': '1',
    '_uetsid': '60cdd09091c711ef8399f5ec510f824c',
    '_uetvid': '8351f910908311efa48421e1f63ace65',
}



headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'sid_key=oxid; visitor_id883653=892544652; visitor_id883653-hash=5754bdd2b4eab77d9963edf2fc0056f55a4e6c146955a24c7a567f585f6e82b7dbb92532fabd963e33fce58d72357b1464c44794; showlinksonce=1; oxid_1_autologin=1; oxid_1=osl%40famaga.de%40%40%40%242y%2410%24dZo31hQK8PfmnWXz13nkhOUZbuSVgWnKYiF3duGW4S9PXFE2JhlJ.; sid=pars0ihmvi1467lbins9nl7ptq; language=1; _uetsid=60cdd09091c711ef8399f5ec510f824c; _uetvid=8351f910908311efa48421e1f63ace65',
    'origin': 'https://shop.murrelektronik.de',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    # 'referer': 'https://shop.murrelektronik.de/en/M23-SERVO-CABLE-7000-PS411-8210300.html',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


def get_sale_price(article):

    data = {
        'artlist[0][artnum]': article,
        'artlist[0][amount]': '1',
        'cl': 'nfc_middleware_user_prices',
        'fnc': 'execute',
        'pageType': 'detail',
    }

    response = requests.post(
        'https://shop.murrelektronik.de/index.php',
        cookies=cookies,
        # headers=headers,
        data=data)

    if "AN ERROR OCCURRED" in str(response.content):
        return ""
    else:
        data = json.loads(response.content)
        sale_price = data["updateListUserPrice"][article]["1"]["price"]
        return sale_price


# print(get_sale_price("7000-40101-6230600"))