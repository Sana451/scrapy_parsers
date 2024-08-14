import csv
import requests
import xml.etree.ElementTree as ET


def get_all_products(url):
    response = requests.get(url)
    tree = ET.fromstring(response.content)
    with open("product_urls.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL"])
        for url_elem in tree.findall(
            "{http://www.sitemaps.org/schemas/sitemap/0.9}url"
        ):
            loc_elem = url_elem.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
            url = loc_elem.text
            writer.writerow([url])
    print("CSV file 'product_urls.csv' created successfully.")
