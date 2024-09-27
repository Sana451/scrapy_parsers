import sys

import requests

sys.path.insert(0, "/home/sana451/PycharmProjects/scrapy_parsers")
from tools import my_scraping_tools as my_tools


def make_post_for_price(product_id: int):
    resp = requests.post("https://www.riegler.de/de/de/erp/reload/data/",
                         data=f'products%5B4%5D%5BproductId%5D={product_id}&form_key=o6yviFzaTLqAbn0R',
                         headers={
                             "accept": "*/*",
                             "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                             "priority": "u=1, i",
                             "referer": "https://www.riegler.de/de/de/filter-futura-mit-pc-behalter-schutzkorb-5-m-bg-4-g-1-ha-100150-2.html",
                             "sec-fetch-dest": "empty",
                             "sec-fetch-mode": "cors",
                             "sec-fetch-site": "same-origin",
                             "x-requested-with": "XMLHttpRequest"
                         },
                         cookies={
                             "PHPSESSID": "ui87dafqnnlof8j3130uqhslj9",
                             "STUID": "416af0d2-bbf8-13a4-9b04-04ff3f060040",
                             "STVID": "e65cdae2-7f49-fd3e-ffcb-21c5a74b875a",
                             "X-Magento-Vary": "5419d2091fac5275c00341aef91aff418768e5c0",
                             "_gcl_au": "1.1.813304060.1727181128",
                             "form_key": "o6yviFzaTLqAbn0R",
                             "mage-banners-cache-storage": "{}",
                             "mage-cache-sessid": "true",
                             "mage-cache-storage": "{}",
                             "mage-cache-storage-section-invalidation": "{}",
                             "mage-messages": "",
                             "persistent_shopping_cart": "uj3dn1UxTyMtBsI2mvVQqldVPmIDAkt46WPqU1whagqDiWs9sK",
                             "private_content_version": "3e23049cb34477fab9d8097b978d1601",
                             "product_data_storage": "{}",
                             "recently_compared_product": "{}",
                             "recently_compared_product_previous": "{}",
                             "recently_viewed_product": "{}",
                             "recently_viewed_product_previous": "{}",
                             "section_data_ids": "{%22company%22:1727245621%2C%22requisition%22:1727245621%2C%22customer-product-data%22:1727247607%2C%22customer%22:1727245607%2C%22compare-products%22:1727245607%2C%22last-ordered-items%22:1727245607%2C%22cart%22:1727245621%2C%22directory-data%22:1727245607%2C%22captcha%22:1727245607%2C%22wishlist%22:1727245607%2C%22company_authorization%22:1727245607%2C%22negotiable_quote%22:1727245607%2C%22instant-purchase%22:1727245607%2C%22loggedAsCustomer%22:1727245607%2C%22multiplewishlist%22:1727245607%2C%22purchase_order%22:1727245607%2C%22persistent%22:1727245607%2C%22review%22:1727245607%2C%22webforms%22:1727245607%2C%22contact-person%22:1727245607%2C%22recently_viewed_product%22:1727245607%2C%22recently_compared_product%22:1727245607%2C%22product_data_storage%22:1727245607%2C%22paypal-billing-agreement%22:1727245607}",
                             "uslk_umm_121658_s": "ewAiAHYAZQByAHMAaQBvAG4AIgA6ACIAMQAiACwAIgBkAGEAdABhACIAOgB7AH0AfQA="
                         },
                         auth=(),
                         )
    js_res = resp.json()[0]
    print(js_res)
    return {"sale_price": js_res["NetValue"],
            "avalabillity": js_res["main_stock_message"]}
    # return resp.json()[0]["NetValue"]
    # return resp.json()[0]["main_stock_message"]


print(make_post_for_price(6230))
