import re
from http.cookies import SimpleCookie
import csv

from bs4 import BeautifulSoup
from tabulate import tabulate


def save_error(url, error, field, err_file_path):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


def cookie_dict_from_string(raw_cookie_str: str) -> dict:
    cookie = SimpleCookie()
    cookie.load(raw_cookie_str)
    cookies = {k: v.value for k, v in cookie.items()}
    return cookies


def del_classes_AND_divs_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    [d.decompose() for d in soup.find_all("div")]

    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name", "aria-label", "role", "colspan"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def del_classes_from_html(html) -> str:
    if not isinstance(html, BeautifulSoup):
        soup = BeautifulSoup(html, "html.parser")
    else:
        soup = html
    for tag in soup():
        for attribute in ["class", "style", "id", "scope", "data-th",
                          "target", "itemprop", "content", "data-description", "data-uid",
                          "data-name", "href", "title", "cellpadding", "cellspacing", "width",
                          "colspan"]:
            del tag[attribute]

    result = re.sub(r'<!.*?->', '', str(soup))  # удалить комментарии
    return result


def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(["class", "style", "id", "scope", "data-th", "target"]):
        data.decompose()

    return ' '.join(soup.stripped_strings)


def create_html_table(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    res = []
    divs = soup.find_all("div")
    for div in divs:
        span_list = div.find_all("span")
        if len(span_list) == 2:
            res.append(i.text.strip() for i in span_list)

    html = tabulate(res, tablefmt="html").replace("\n", "")

    return html
