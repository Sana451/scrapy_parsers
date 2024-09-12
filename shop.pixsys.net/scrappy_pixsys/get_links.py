# from bs4 import BeautifulSoup
# import requests
# import csv
#
# #
# # with open("/home/sana451/PycharmProjects/scrapy_parsers/shop.pixsys.net/scrappy_pixsys/results/category_links.csv") as csvfile:
# #     reader = csv.reader(csvfile)
# #     cat_links = list(reader)
# #
# # with open("/home/sana451/PycharmProjects/scrapy_parsers/shop.pixsys.net/scrappy_pixsys/results/product_links.csv", "a") as csvfile:
# #     writer = csv.writer(csvfile)
# #     for link in cat_links:
# #         cat_page = requests.get(link[0])
# #         soup = BeautifulSoup(cat_page.content)
# #         divs = soup.select("div.item-griglia")
# #         hrefs = [div.find('a')['href'] for div in divs]
# #         for href in hrefs:
# #             writer.writerow([href])
#
# soup = BeautifulSoup(requests.get("https://shop.pixsys.net/en/").content)
#
# res = []
#
# categories = categories = soup.select("div#categories_block_left")[0].select(".block_content")[0].select("ul.tree")[
#     0].select("ul")
# li = [[a['href'] for a in cat.select('a')] for cat in categories]
# for i in li:
#     res.extend(i)
#
# res.append("https://shop.pixsys.net/en/805-signal-converters")
#
# print(res)
#
# all_product_links = []
#
# for cat_page in res:
#     soup = BeautifulSoup(requests.get(cat_page).content)
#     product_links = [a['href'] for a in soup.select("a.product-name")]
#     all_product_links.extend(product_links)
#
