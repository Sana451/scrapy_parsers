import pandas
import requests
from bs4 import BeautifulSoup

DOMAIN = "https://www.steute-controltec.com"

# response = requests.get("https://www.steute-controltec.com/de/produkte")
# soup = BeautifulSoup(response.content, "html.parser")
#
# cats = [DOMAIN + a["href"] for a in soup.select("a.stretched-link")]
#
# print(cats)

cats = [
    'https://www.steute-controltec.com/de/produkte/fussschalter',
    'https://www.steute-controltec.com/de/produkte/sicherheitsfussschalter',
    'https://www.steute-controltec.com/de/produkte/seilzugschalter',
    'https://www.steute-controltec.com/de/produkte/seilzug-notschalter',
    'https://www.steute-controltec.com/de/produkte/sicherheitsschalter-mit-getrenntem-betaetiger',
    'https://www.steute-controltec.com/de/produkte/sicherheitsschalter-fuer-drehbare-schutzeinrichtungen',
    'https://www.steute-controltec.com/de/produkte/tuerkontakte-fuer-aufzugtueren',
    'https://www.steute-controltec.com/de/produkte/induktivsensoren',
    'https://www.steute-controltec.com/de/produkte/magnetsensoren',
    'https://www.steute-controltec.com/de/produkte/optische-sensoren',
    'https://www.steute-controltec.com/de/produkte/sicherheitssensoren',
    'https://www.steute-controltec.com/de/produkte/positionsschalter',
    'https://www.steute-controltec.com/de/produkte/miniaturendschalter',
    'https://www.steute-controltec.com/de/produkte/schlaffseilschalter',
    'https://www.steute-controltec.com/de/produkte/hubendschalter',
    'https://www.steute-controltec.com/de/produkte/handbediengeraete',
    'https://www.steute-controltec.com/de/produkte/befehlsgeraete',
    'https://www.steute-controltec.com/de/produkte/sicherheitszuhaltungen',
    'https://www.steute-controltec.com/de/produkte/bandschieflaufschalter',
    'https://www.steute-controltec.com/de/produkte/bandriss-ueberwachungsschalter',
    'https://www.steute-controltec.com/de/produkte/multifunktionsgriffe',
    'https://www.steute-controltec.com/de/produkte/funk-universalsender',
    'https://www.steute-controltec.com/de/produkte/funk-empfaenger-und-funk-repeater',
    'https://www.steute-controltec.com/de/produkte/zubehoer',
    'https://www.steute-controltec.com/de/produkte/ex-schaltgeraete-und-ex-sensoren',
    'https://www.steute-controltec.com/de/produkte/funk-schaltgeraete-und-funk-sensoren',
    'https://www.steute-controltec.com/de/produkte/sicherheitsschaltgeraete-und-sicherheitssensoren'
]

cookies = {
    'fe_typo_user': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiYmI5ZjM4ODI5OWNlOTQyNDBkZDZkN2NmZmUwZTU2YzciLCJ0aW1lIjoiMjAyNC0xMC0xOVQxMzo1MToyNiswMjowMCIsInNjb3BlIjp7ImRvbWFpbiI6Ind3dy5zdGV1dGUtY29udHJvbHRlYy5jb20iLCJob3N0T25seSI6dHJ1ZSwicGF0aCI6Ii8ifX0.ySomuOqh6Zx2-vv2fFxlx8C4uTRGVlDlWjcn413LMu8',
    'staticfilecache': 'typo_user_logged_in',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7',
    'cache-control': 'no-cache',
    # 'content-length': '0',
    # 'cookie': 'fe_typo_user=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGlmaWVyIjoiYmI5ZjM4ODI5OWNlOTQyNDBkZDZkN2NmZmUwZTU2YzciLCJ0aW1lIjoiMjAyNC0xMC0xOVQxMzo1MToyNiswMjowMCIsInNjb3BlIjp7ImRvbWFpbiI6Ind3dy5zdGV1dGUtY29udHJvbHRlYy5jb20iLCJob3N0T25seSI6dHJ1ZSwicGF0aCI6Ii8ifX0.ySomuOqh6Zx2-vv2fFxlx8C4uTRGVlDlWjcn413LMu8; staticfilecache=typo_user_logged_in',
    'origin': 'https://www.steute-controltec.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.steute-controltec.com/de/produkte/fussschalter',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

prod_links = set()

for url in cats[:]:
    print(url)
    page_num = 1
    while True:
        print("Page: ", page_num)

        params = {
            'tx_solr[filter][0]': 'type:tx_ofproduct_domain_model_article',
            'tx_solr[page]': page_num,
        }

        response = requests.post(
            url=url,
            params=params,
            cookies=cookies,
            headers=headers,
        )

        soup = BeautifulSoup(response.content, "html.parser")

        links = [DOMAIN +
                 a["href"] for a in soup.select(".solr-list__results a.stretched-link") if
                 "mehr Produkte" not in a.text]
        prod_links.update(links)
        print(len(links))
        if "mehr Produkte" in soup.text:
            page_num += 1
        else:
            break

print(len(prod_links))

pandas.DataFrame(prod_links).to_csv(
    "/steute_controltec_com/steute_controltec_com/results/steute-controltec.com.links.csv",
    index=False)
