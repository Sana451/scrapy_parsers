import requests
from bs4 import BeautifulSoup
import pandas

categories = [
    "https://www.aircom.net/de/druckregler,2.html",
    "https://www.aircom.net/de/volumenstrombooster,4.html",
    "https://www.aircom.net/de/proportionaldruckregler,3.html",
    "https://www.aircom.net/de/volumenstromregelung,5.html",
    "https://www.aircom.net/de/druckbegrenzungsventile,22.html",
    "https://www.aircom.net/de/druckschalter,8.html",
    "https://www.aircom.net/de/druckmessumformer,11.html",
    "https://www.aircom.net/de/druckmessgeraete,10.html",
    "https://www.aircom.net/de/edelstahlgeraete,6.html",
    "https://www.aircom.net/de/druckluftaufbereitung,7.html",
    "https://www.aircom.net/de/druckerhoeher,30.html",
    "https://www.aircom.net/de/schutzbauteile,500.html",
    "https://www.aircom.net/de/zubehoer,629.html"
]
#
# all_sub_cats = []
#
# for cat in categories[:]:
#     resp = requests.get(cat)
#     soup = BeautifulSoup(resp.content, "html.parser")
#     sub_cats = [a["href"] for a in soup.select(".startpage-productgroups a")]
#     all_sub_cats.extend(sub_cats)
#
# # print(len(all_sub_cats))
# print(all_sub_cats)

sub_cats = ['https://www.aircom.net/de/miniaturdruckregler,16.html',
            'https://www.aircom.net/de/standarddruckregler,13.html',
            'https://www.aircom.net/de/niederdruckregler,15.html', 'https://www.aircom.net/de/hochdruckregler,14.html',
            'https://www.aircom.net/de/praezisionsdruckregler,27.html',
            'https://www.aircom.net/de/vakuumdruckregler,21.html',
            'https://www.aircom.net/de/differenzdruckregler,17.html',
            'https://www.aircom.net/de/mechanisch-betaetigt,614.html',
            'https://www.aircom.net/de/flaschendruckregler,18.html',
            'https://www.aircom.net/de/wasserdruckregler,19.html',
            'https://www.aircom.net/de/dampfdruckregler,20.html', 'https://www.aircom.net/de/druckminderer,118.html',
            'https://www.aircom.net/de/wartungseinheiten-fr-f-oe,124.html',
            'https://www.aircom.net/de/druckbegrenzer,120.html',
            'https://www.aircom.net/de/booster,119.html', 'https://www.aircom.net/de/filterregler,121.html',
            'https://www.aircom.net/de/filter,122.html', 'https://www.aircom.net/de/oeler,123.html',
            'https://www.aircom.net/de/volumenstromregelung,125.html',
            'https://www.aircom.net/de/druckluftfilter,23.html',
            'https://www.aircom.net/de/filterdruckregler,24.html', 'https://www.aircom.net/de/druckluftoeler,25.html',
            'https://www.aircom.net/de/wartungsgeraete,26.html', 'https://www.aircom.net/de/zubehoer,29.html',
            'https://www.aircom.net/de/hoseguard,512.html', 'https://www.aircom.net/de/in-line-regler-toolreg,616.html',
            'https://www.aircom.net/de/in-line-regler-cartreg,619.html',
            'https://www.aircom.net/de/in-line-regler-saveair,622.html',
            'https://www.aircom.net/de/in-line-regler-ecoreg,628.html',
            "https://www.aircom.net/de/volume-boosters,4.html",
            "https://www.aircom.net/de/proportionaldruckregler,3.html",
            "https://www.aircom.net/de/volumenstromregelung,5.html",
            "https://www.aircom.net/de/druckbegrenzungsventile,22.html",
            "https://www.aircom.net/de/druckschalter,8.html",
            "https://www.aircom.net/de/druckmessumformer,11.html",
            "https://www.aircom.net/de/druckmessgeraete,10.html",
            "https://www.aircom.net/de/druckerhoeher,30.html",
            "https://www.aircom.net/de/zubehoer,629.html"

            ]

# print(len(sub_cats))
all_prod_links = []

for sub_cat in sub_cats:
    resp = requests.get(sub_cat)
    soup = BeautifulSoup(resp.content, "html.parser")
    products = soup.select(".product-container a")
    product_links = [a["href"].strip() for a in products]
    all_prod_links.extend(product_links)


print(all_prod_links)
print(len(all_prod_links))

pandas.DataFrame(all_prod_links
                 ).to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/aircom_net/aircom_net/results/links.aircom.csv",
    index=False
)
