import random
import time
from playwright.sync_api import sync_playwright
from cookie import cookie


def click_first_link_and_input():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        # Add the cookiess
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        ]
        random_user_agent = random.choice(user_agents)
        # context.set_extra_http_headers(
        #     {
        #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        #         "Accept-Encoding": "gzip, deflate, br, zstd",
        #         "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        #         "Connection": "keep-alive",
        #         "Cookie": cookie,
        #         "Host": "www.schmalz.com",
        #         "Priority": "u=0, i",
        #         "Sec-Fetch-Dest": "document",
        #         "Sec-Fetch-Mode": "navigate",
        #         "Sec-Fetch-Site": "same-origin",
        #         "Sec-Fetch-User": "?1",
        #         "TE": "trailers",
        #         "Upgrade-Insecure-Requests": "1",
        #         "User-Agent": random_user_agent,
        #     }
        # )
        # context.add_cookies(
        #     [
        #         {
        #             "name": "OAuth_Token_Request_State",
        #             "value": "ed4176cd-54e4-4cd2-abee-d6f606fff5af",
        #             "domain": "www.schmalz.com",
        #             "path": "/",
        #         },
        #         {
        #             "name": "loggedIn",
        #             "value": "true",
        #             "domain": ".www.schmalz.com",
        #             "path": "/",
        #         },
        #         {
        #             "name": "JSESSIONID",
        #             "value": "33F475BEB13430C97778863B22546E59",
        #             "domain": "www.schmalz.com",
        #             "path": "/",
        #         },
        #     ]
        # )

        page = context.new_page()

        # Set a timeout for loading the page
        page.set_default_timeout(10000)  # 10 seconds

        # Try to load the page, and refresh if it doesn't load within the timeout\
        while True:
            try:
                page.goto("https://www.schmalz.com/en-de/")
                break
            except:
                print("Page didn't load within the timeout, refreshing...")
                page.reload()

        time.sleep(5)
        print("after sleep")
        page.click(
            "#uc-center-container > div.sc-eBMEME.dRvQzh > div > div.sc-jsJBEP.bHqEwZ > div > button:nth-child(3)"
        )
        # Click the first link under the ".user-header-icon > a" selector
        page.click(".user-header-icon > a:nth-child(1)")
        time.sleep(5)
        page.click(".btn-primary")
        # ! изменить ввод, сделать через .env
        page.fill("#username", "jk@famaga.de")
        page.fill("#password", "Famaga2022")
        # Get the current URL after clicking the link
        time.sleep(5)
        page.click("#kc-login")
        time.sleep(5)
        current_url = page.url

        context.close()
        browser.close()
        return current_url


current_url = click_first_link_and_input()
print(f"Current URL: {current_url}")
