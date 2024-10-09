import csv
import time

import requests
from bs4 import BeautifulSoup


def get_request_1(id, page_num):
    # data = {"selected": {}, "page": page_num}
    # print(data, id)
    # response = requests.post(f"https://air-com.pl/ajax/store/product/filters/get/{id}",
    #                          data=data,
    response = requests.post("https://air-com.pl/ajax/store/product/filters/get/38472",
                             data='{"selected":{},"page":8}',
                             headers={
                                 "accept": "*/*",
                                 "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
                                 "cache-control": "no-cache",
                                 "content-type": "application/json",
                                 "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQzMzA3NTUiLCJhcCI6IjUzODU1NzU1MyIsImlkIjoiZjA4NWFiY2VkZTdlNTk4YiIsInRyIjoiMDhmZDdmMzNkNmU1NGQ1ZWE0ZjVkNWQ5YzQ3ZDkzY2QiLCJ0aSI6MTcyODAzNjE4OTIxMn19",
                                 "origin": "https://air-com.pl",
                                 "pragma": "no-cache",
                                 "priority": "u=1, i",
                                 "referer": "https://air-com.pl/p/elektrozawory-sterowane-bezposrednio-22-32-nz-no-seria-a-camozzi,38472",
                                 "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
                                 "sec-ch-ua-arch": "\"x86\"",
                                 "sec-ch-ua-bitness": "\"64\"",
                                 "sec-ch-ua-full-version": "\"127.0.6533.119\"",
                                 "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"127.0.6533.119\", \"Chromium\";v=\"127.0.6533.119\"",
                                 "sec-ch-ua-mobile": "?0",
                                 "sec-ch-ua-model": "\"\"",
                                 "sec-ch-ua-platform": "\"Linux\"",
                                 "sec-ch-ua-platform-version": "\"6.8.0\"",
                                 "sec-fetch-dest": "empty",
                                 "sec-fetch-mode": "cors",
                                 "sec-fetch-site": "same-origin",
                                 "traceparent": "00-08fd7f33d6e54d5ea4f5d5d9c47d93cd-f085abcede7e598b-01",
                                 "tracestate": "4330755@nr=0-1-4330755-538557553-f085abcede7e598b----1728036189212",
                                 "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                                 "x-csrf-token": "YpZK08voMSwobB7zqNs9wsFHRXj9yJn7RNYby9XG"
                             },
                             cookies={
                                 "CookieConsent": "{stamp:%27JQIkf7UP0B6BxdKr5zyQHPDoqajqAk/F7WwM15BuygszRISPfhUspw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1728022679455%2Cregion:%27ru%27}",
                                 "XSRF-TOKEN": "YpZK08voMSwobB7zqNs9wsFHRXj9yJn7RNYby9XG",
                                 "_clck": "11ep28v%7C2%7Cfpq%7C0%7C1738",
                                 "_clsk": "gr6zu0%7C1728036186773%7C29%7C1%7Cp.clarity.ms%2Fcollect",
                                 "_ga": "GA1.2.1238113704.1728022599",
                                 "_gat_UA-35078555-1": "1",
                                 "_gcl_au": "1.1.419109824.1728022679",
                                 "_gid": "GA1.2.1367082428.1728022679",
                                 "_uetsid": "6760e650821811efa0fe5fbb5a3f7dc5",
                                 "_uetvid": "67611cc0821811efad50fd88763518c3",
                                 "cf_chl_rc_m": "1",
                                 "cf_clearance": "FK7mLGmB98JuA_PZYeUqQIc0C5ROrShpleepMyjEH3g-1728035908-1.2.1.1-cXkyNMbsTrulGt.P0dki0tjfHY2vLKldJzzgrM00tySHsoxc5lr5sPUHp1jxS6i6xDzn_EV95GAAsuapDXbJERDWWSd7ApdTm.Oz_Q6QRwJSLUtQTiowFmvvyY6qFrUMQZVpdC1DUX5qiyjELUs848rfhm_7_rLpd2M90L9gGuusGEW1tpdadq2PEGupWek8EtzbYDCHsf7JHBi3y4spO51WTUsvcTd6EAxPao7JFgj5krRvMwj34lTMmqOagaQNmpTrCsmBeWamOUiOZlz3cYVBAy8qjsKj.lmSb9980OLvcNE71ofgHdbp_qjuRPyHf8BIpHyzf10bDr_PjFU9NxQXlsqCJKaJCel88vT3N8QF7NPdhnFuVAb_UbTyvOsSWSKmyDYs.UpWE72bRTJSUVD8cx8vSbEJBdw_TPs4xS8",
                                 "user_session": "eyJpdiI6ImdMMEx3VmdXcE5TQTVUa1BiZklyWWc9PSIsInZhbHVlIjoieUZneFVJZnhudkxZT3JtSmFubzJoWFlSVitJbjNRZVlUbWhTNFE4UHZzejZoZDNkMkdWMWlPNUh5WlVWOUZjL1FsZ3Q4blduOUZ1MXFsSE1XVjFHOWR2Nk5DS2FiRmJ6end2QUYyNUhiYk5URU95QXhrdjNPcHE1VmRnUjJ6cGQiLCJtYWMiOiIxZDUzZjkyMjk1OWY4MjhjMzIyNGYwNDE3YjRhMDJjZTAwYjI0Y2JmNjc1YmY0YmYyNDk4ZTZlY2JmZWE3YzUyIiwidGFnIjoiIn0%3D"
                             },
                             auth=(),
                             )
    return response


def get_request_2(id, page_num):
    # data = {"selected": {}, "page": page_num}
    # print(data, id)
    # response = requests.post(f"https://air-com.pl/ajax/store/product/filters/get/{id}",
    #                          data=data,
    response = requests.post("https://air-com.pl/ajax/store/product/filters/get/38472",
                             data='{"selected":{},"page":3}',
                             headers={
                                 "accept": "*/*",
                                 "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
                                 "cache-control": "no-cache",
                                 "content-type": "application/json",
                                 "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQzMzA3NTUiLCJhcCI6IjUzODU1NzU1MyIsImlkIjoiM2U1OTlkZjFlNTQzNTRjMiIsInRyIjoiZjBlNjZiNjU2ODA1ZTM4NjhkZjVkNGU0ZmE2MzEzMDMiLCJ0aSI6MTcyODAzNjI4MTE0Mn19",
                                 "origin": "https://air-com.pl",
                                 "pragma": "no-cache",
                                 "priority": "u=1, i",
                                 "referer": "https://air-com.pl/p/elektrozawory-sterowane-bezposrednio-22-32-nz-no-seria-a-camozzi,38472",
                                 "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
                                 "sec-ch-ua-arch": "\"x86\"",
                                 "sec-ch-ua-bitness": "\"64\"",
                                 "sec-ch-ua-full-version": "\"127.0.6533.119\"",
                                 "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"127.0.6533.119\", \"Chromium\";v=\"127.0.6533.119\"",
                                 "sec-ch-ua-mobile": "?0",
                                 "sec-ch-ua-model": "\"\"",
                                 "sec-ch-ua-platform": "\"Linux\"",
                                 "sec-ch-ua-platform-version": "\"6.8.0\"",
                                 "sec-fetch-dest": "empty",
                                 "sec-fetch-mode": "cors",
                                 "sec-fetch-site": "same-origin",
                                 "traceparent": "00-f0e66b656805e3868df5d4e4fa631303-3e599df1e54354c2-01",
                                 "tracestate": "4330755@nr=0-1-4330755-538557553-3e599df1e54354c2----1728036281142",
                                 "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                                 "x-csrf-token": "YpZK08voMSwobB7zqNs9wsFHRXj9yJn7RNYby9XG"
                             },
                             cookies={
                                 "CookieConsent": "{stamp:%27JQIkf7UP0B6BxdKr5zyQHPDoqajqAk/F7WwM15BuygszRISPfhUspw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1728022679455%2Cregion:%27ru%27}",
                                 "XSRF-TOKEN": "YpZK08voMSwobB7zqNs9wsFHRXj9yJn7RNYby9XG",
                                 "_clck": "11ep28v%7C2%7Cfpq%7C0%7C1738",
                                 "_clsk": "gr6zu0%7C1728036186773%7C29%7C1%7Cp.clarity.ms%2Fcollect",
                                 "_ga": "GA1.2.1238113704.1728022599",
                                 "_gat_UA-35078555-1": "1",
                                 "_gcl_au": "1.1.419109824.1728022679",
                                 "_gid": "GA1.2.1367082428.1728022679",
                                 "_uetsid": "6760e650821811efa0fe5fbb5a3f7dc5",
                                 "_uetvid": "67611cc0821811efad50fd88763518c3",
                                 "cf_chl_rc_m": "1",
                                 "cf_clearance": "FK7mLGmB98JuA_PZYeUqQIc0C5ROrShpleepMyjEH3g-1728035908-1.2.1.1-cXkyNMbsTrulGt.P0dki0tjfHY2vLKldJzzgrM00tySHsoxc5lr5sPUHp1jxS6i6xDzn_EV95GAAsuapDXbJERDWWSd7ApdTm.Oz_Q6QRwJSLUtQTiowFmvvyY6qFrUMQZVpdC1DUX5qiyjELUs848rfhm_7_rLpd2M90L9gGuusGEW1tpdadq2PEGupWek8EtzbYDCHsf7JHBi3y4spO51WTUsvcTd6EAxPao7JFgj5krRvMwj34lTMmqOagaQNmpTrCsmBeWamOUiOZlz3cYVBAy8qjsKj.lmSb9980OLvcNE71ofgHdbp_qjuRPyHf8BIpHyzf10bDr_PjFU9NxQXlsqCJKaJCel88vT3N8QF7NPdhnFuVAb_UbTyvOsSWSKmyDYs.UpWE72bRTJSUVD8cx8vSbEJBdw_TPs4xS8",
                                 "user_session": "eyJpdiI6InhFRER0eHdwbEU5dnhnRmlPa1h6ZGc9PSIsInZhbHVlIjoiSkdjNC94a29uMjU5V0RmWHdxSHUzNWRKNE1iTXlZaFNyWXp4cFNFMndYejFOUXJwQ1BhcXdYbW8wNTFHcnVOKzIvTUhVeU53QmppYytFRm84NTAwWUtPTUVuY2p4VXR1MjV1RWp3WnVpS2hiTDVqWVMrSUt2dE8raDdjMTZWTy8iLCJtYWMiOiI5MjY5N2Q0OTRjODE0YTlkMGVkNWYyNzAzMzU0MGEwNWQwNWMxMDAyMjlmMDBlYjFjOGVkMDU0ZWU0ZmZkNWNmIiwidGFnIjoiIn0%3D"
                             },
                             auth=(),
                             )
    return response


for i in range(9, 251):
    resp = get_request_1("38472", 1)
    print(resp.status_code)
    soup = BeautifulSoup(resp.json()["products_list_view"], "html.parser")
    links = soup.select(".variants-cell--name a")
    links = [["https://air-com.pl" + l["href"]] for l in links]
    print(links)
    time.sleep(10)

    with open("/home/sana451/PycharmProjects/scrapy_parsers/air_com_pl/air_com_pl/results/air-com.pl.camozzi.links.csv",
              "a") as file:
        writer = csv.writer(file)
        for link in links:
            writer.writerow(link)

#
# resp = get_request_2("38472", 2)
# print(resp.status_code)
# soup = BeautifulSoup(resp.json()["products_list_view"], "html.parser")
# links = soup.select(".variants-cell--name a")
# links = [["https://air-com.pl" + l["href"]] for l in links]
# print(links)
