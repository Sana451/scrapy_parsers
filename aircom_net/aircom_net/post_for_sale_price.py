import sys

import requests

sys.path.insert(0, "/")
from tools import my_scraping_tools as my_tools

import uncurl

# print(uncurl.parse(r"""curl 'https://www.aircom.net/de/Gruppe/r364,175/r364-010,3178.htm'   -H 'Accept: text/javascript, text/html, application/xml, text/xml, */*'   -H 'Accept-Language: ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7'   -H 'Cache-Control: no-cache'   -H 'Connection: keep-alive'   -H 'Content-type: application/x-www-form-urlencoded; charset=UTF-8'   -H 'Cookie: i_ProductGroupId=30; CookieConsent={stamp:%27WhbVbjbr0V/Ja2MemL2Pb7eJh8BT+SCiGuoO/n7SY5mfej/9w2j3Dw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1727330583692%2Cregion:%27ru%27}; PHPSESSID=4irpulein7qjb15j8k5qjjhtni'   -H 'Origin: https://www.aircom.net'   -H 'Pragma: no-cache'   -H 'Referer: https://www.aircom.net/de/miniaturdruckregler/r364,175.html'   -H 'Sec-Fetch-Dest: empty'   -H 'Sec-Fetch-Mode: cors'   -H 'Sec-Fetch-Site: same-origin'   -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'   -H 'X-Prototype-Version: 1.7'   -H 'X-Requested-With: XMLHttpRequest'   -H 'sec-ch-ua: "Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"'   -H 'sec-ch-ua-mobile: ?0'   -H 'sec-ch-ua-platform: "Linux"'   --data-raw 'bForAjax=1&sHint=0'"""))
prod_info = ['7268', '1736', '231a0220', '231']


def make_post_sale_price():
    resp = requests.post(
        url=f"https://www.aircom.net/de/Gruppe/{prod_info[3]},{prod_info[1]}/{prod_info[2]},{prod_info[0]}.htm",
        # resp = requests.post("https://www.aircom.net/de/Gruppe/r364,175/r364-010,3178.htm",
        data='bForAjax=1&sHint=0',
        headers={
            "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
            "Accept-Language": "ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.aircom.net",
            "Pragma": "no-cache",
            "Referer": "https://www.aircom.net/de/miniaturdruckregler/r364,175.html",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "X-Prototype-Version": "1.7",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\""
        },
        cookies={
            "CookieConsent": "{stamp:%27WhbVbjbr0V/Ja2MemL2Pb7eJh8BT+SCiGuoO/n7SY5mfej/9w2j3Dw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1727330583692%2Cregion:%27ru%27}",
            "PHPSESSID": "4irpulein7qjb15j8k5qjjhtni",
            "i_ProductGroupId": "30"
        },
        auth=(),
    )
    return resp.content


make_post_sale_price()
