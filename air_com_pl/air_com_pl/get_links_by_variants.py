import csv

import requests
from bs4 import BeautifulSoup
import pandas


# url = f"https://air-com.pl/ajax/store/product/filters/get/{id}"
# data=data,


def get_request(id, page_num):
    data = f"""'{{"selected":{{}},"page":{page_num}}}'""".strip("'")
    print(data, id)
    response = requests.post(f"https://air-com.pl/ajax/store/product/filters/get/{id}",
                             data=data,
                             headers={
                                 "accept": "*/*",
                                 "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
                                 "cache-control": "no-cache",
                                 "content-type": "application/json",
                                 "newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjQzMzA3NTUiLCJhcCI6IjUzODU1NzU1MyIsImlkIjoiMDJlODU1NDNlYjRkMTJjYiIsInRyIjoiODZjODgwOWM5YzdjYTNkODg5MTM1OTgzMzZhYTMxZGMiLCJ0aSI6MTcyODA1MzI4NDMwMH19",
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
                                 "traceparent": "00-86c8809c9c7ca3d88913598336aa31dc-02e85543eb4d12cb-01",
                                 "tracestate": "4330755@nr=0-1-4330755-538557553-02e85543eb4d12cb----1728053284300",
                                 "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                                 "x-csrf-token": "YpZK08voMSwobB7zqNs9wsFHRXj9yJn7RNYby9XG"
                             },
                             cookies={
                                 "CookieConsent": "{stamp:%27JQIkf7UP0B6BxdKr5zyQHPDoqajqAk/F7WwM15BuygszRISPfhUspw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1728022679455%2Cregion:%27ru%27}",
                                 "XSRF-TOKEN": "YpZK08voMSwobB7zqNs9wsFHRXj9yJn7RNYby9XG",
                                 "_clck": "11ep28v%7C2%7Cfpq%7C0%7C1738",
                                 "_ga": "GA1.2.1238113704.1728022599",
                                 "_gat_UA-35078555-1": "1",
                                 "_gcl_au": "1.1.419109824.1728022679",
                                 "_gid": "GA1.2.1367082428.1728022679",
                                 "_uetsid": "6760e650821811efa0fe5fbb5a3f7dc5",
                                 "_uetvid": "67611cc0821811efad50fd88763518c3",
                                 "cf_clearance": "mHneRN4PHkARCB7zetntf7qKJnJuCred3nlMq2US96A-1728053272-1.2.1.1-jqIvFJhIyxoZUBwLU8rBD9LC5uJZ5Y_cpUXaRbp8NsV4ZdKOKhhGKT4yD9QP7NMsJaHoK7cpMUAonv.nxdCukmrDALG7q1rAOCFCuA1z5n6FubOy0tuv4f4Yhs5fOmVHDpWQYi5q_enYg6dupQl1ugnER0FORa4tXXsmeviOWJA8pB4kD_pFP.lWd0Afdd8j3cVbJshc_d9LySMeY_pvXmIyt_pn2.njxpp9OMXaY7jZC8SL1JUBUH5M2X4YCZ3zJtrSqrpQrFs4c2TAhVkYsEV0Pg9E27X58PRr3EntRjfgyx_Jizru06X9mkmbyNGcmpw8YJqF_PA0FtbYQcGSM04g5bAk2aqPC6XmOCxAabh02zGdm0jYQSKCZl4rDOApoemTCnXZZFXUteEOZ3iRRh1auM18ohs3JCLyiqonjqw",
                                 "user_session": "eyJpdiI6IjV6bExsOWJRaEwzN0kvaGJzeStHNUE9PSIsInZhbHVlIjoibStXN1FHNVJHSmFiamtNdW10Mk1lR25MT0dPcnpxWnFFeEE3MlAvckNWWHRNZ0l0Z1F2bVFJUklENEtVSkkxVmdaNzU2QkEwMDMwZ0tsRUI2T0xqYUZTbkFpS3ZFbWlFeHRGbHBrbU1GU1NZNUsxSDBSQ3NickFqQzk4Ri9naHgiLCJtYWMiOiJkNTVlYWVjOGE5NmViMWQyYTE4ZjAyM2YyZGNiYTRhODFkYTFiZDVhMmU0MjQ5YWJjMzdiODI3OThkNjRkYWUwIiwidGFnIjoiIn0%3D"
                             },
                             auth=(),
                             )

    return response


all_links_count = 0

if __name__ == '__main__':

    with open("/home/sana451/PycharmProjects/scrapy_parsers/air_com_pl/air_com_pl/results/variants.links.csv",
              "r") as vars_csv_file:
        reader = csv.reader(vars_csv_file)
        urls = [url[0] for url in list(reader)[1:]]
        ids = [url.split(",")[-1] for url in urls]

    with open("/home/sana451/PycharmProjects/scrapy_parsers/air_com_pl/air_com_pl/results/air-com.pl.camozzi.links.csv",
              "a") as links_csv_file:
        writer = csv.writer(links_csv_file)

        forbiden = False
        for id in ids[209:]:
            if forbiden == True:
                break
            print(id)
            page_num = 1
            while True:
                print(page_num)
                resp = get_request(id, page_num)
                if resp.status_code != 200:
                    print("Статус код: ", resp.status_code, "id: ", id, "страница: ", page_num)
                    forbiden = True
                    break
                soup = BeautifulSoup(resp.json()["products_list_view"], "html.parser")
                links = soup.select(".variants-cell--name a")
                links = [["https://air-com.pl" + l["href"]] for l in links]
                for link in links:
                    writer.writerow(link)
                all_links_count += len(links)
                print(len(links), f"Всего: {all_links_count}")

                print("Is more: ", resp.json()["is_more"], "Prod_count: ", resp.json()["products_count"])
                if resp.json()["is_more"] is False:
                    print(resp.json()["is_more"])
                    print("End of category++++++++++++++++++++++++")
                    break
                else:
                    page_num += 1

# pandas.DataFrame(all_links).to_csv(
#     "/home/sana451/PycharmProjects/scrapy_parsers/air_com_pl/air_com_pl/results/air-com.pl.camozzi.links.csv",
#     index=False)
