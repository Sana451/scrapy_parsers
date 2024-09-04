import csv
import bs4

from tabulate import tabulate


#
# soup = bs4.BeautifulSoup(
#     open(
#         "/home/sana451/PycharmProjects/scrapy_norelem/parsers/shop_norelem/shop_norelem/results/1.html",
#         "r",
#     ).read(),
#     "html.parser",
# )

def create_html_table(html: str) -> str:
    soup = bs4.BeautifulSoup(html, "html.parser")

    #     for tag in soup():
    #         for attribute in ["class"]:
    #             del tag[attribute]
    res = []
    for span in soup.find_all("span"):
        res.append((span.text, span.findNext().text))

    return tabulate(res, tablefmt="html").replace("\n", "")


# lst = [i for i in soup.text.split("\n") if i != ""]
# print(lst)
# #
# table = [(lst[i], lst[i + 1]) for i in range(0, len(lst), 2)]
# print(table)
#
# html = tabulate(table, tablefmt="html")
# import csv
#
with open("new_res3.csv", "w", newline="") as new_csvfile:
    writer = csv.writer(new_csvfile, delimiter=",")

    with open("my_results.csv", "r") as old_csvfile:
        reader = csv.reader(old_csvfile)
        data = list(reader)
        writer.writerow(data[0])
        for i in range(1, len(data)):
            # soup = bs4.BeautifulSoup(data[i][7], "html.parser")
            # for tag in soup():
            #     for attribute in ["class"]:
            #         del tag[attribute]
            data[i][7] = create_html_table(data[i][7])
            writer.writerow(data[i])
    # lst = [i for i in soup.text.split("\n") if i != ""]
    # print(lst)
    # table = [(lst[i], lst[i + 1]) for i in range(0, len(lst), 2)]
    # for i in range(0, len(lst), 2):
    #     print(i, i + 1)
    #     print((lst[i], lst[i + 1]))
    # html = tabulate(soup, tablefmt="html")
    # print(html)

# print(data[-1][7])
#
# for row in links_data[1:]:  # Первый элемент - названия полей
#     page_url = row[0]
