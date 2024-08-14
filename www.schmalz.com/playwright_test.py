from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor
import csv
import random
import time
from typing import Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from cookie import cookie
from multiprocessing import Queue
from dotenv import load_dotenv
import os
from check_get_all_product_url import get_all_products

load_dotenv()
USERNAME: str | None = os.getenv("USERNAME_PARSER")
PASSWORD: str | None = os.getenv("PASSWORD_PARSER")


def read_urls_from_csv(path_to_file):
    try:
        with open(f"{path_to_file}", "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                yield row[0]
    except StopIteration:
        print("All URLs have been processed.")
        raise StopIteration("All URLs have been processed.")
    except Exception as e:
        print(e)
        raise e


def fill_untill_max(queue: Queue, url_iter: Iterator):
    while not queue.full():
        try:
            queue.put(url_iter.__next__())
        except StopIteration:
            print("All URLs have been processed.")
            raise StopIteration("All URLs have been processed.")
        except Exception as e:
            print(e)
            raise e


class playwright_parser:
    def __init__(self, queue: Queue, path_to_file: str, url_iter: Iterator):
        self.queue: Queue = queue
        self.queue_iter: Iterator = iter(self.queue.get, None)
        self.path: str = path_to_file
        self.url_iter: Iterator = url_iter

    def check_get(self):
        print(self.queue_iter.__next__())

    def init_login(self):
        while True:
            with sync_playwright() as p:
                browser: Browser = p.chromium.launch(headless=False)
                context: BrowserContext = browser.new_context()
                # Add the cookiess
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
                ]
                random_user_agent = random.choice(user_agents)
                context.set_extra_http_headers(
                    {
                        "User-Agent": random_user_agent,
                    }
                )
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

                page.set_default_timeout(10000)
                while True:
                    try:
                        page.goto("https://www.schmalz.com/en-de/")
                        break
                    except Exception:
                        print("Page didn't load within the timeout, refreshing...")
                        page.reload()

                time.sleep(5)
                print("after sleep")
                page.click(
                    "#uc-center-container > div.sc-eBMEME.dRvQzh > div > div.sc-jsJBEP.bHqEwZ > div > button:nth-child(3)"
                )
                page.click(".user-header-icon > a:nth-child(1)")
                time.sleep(5)
                page.click(".btn-primary")
                if not USERNAME or not PASSWORD:
                    raise Exception("Нет данных пользователя")
                page.fill("#username", USERNAME)
                page.fill("#password", PASSWORD)
                time.sleep(5)
                page.click("#kc-login")
                time.sleep(5)
                print(page.url)
                # context.close()
                # browser.close()
                print(type(browser))
                print(type(context))
                print(type(page))
                yield browser, context, page

    def start_requests(self):
        init_login_gen = self.init_login()
        while True:
            try:
                browser, context, page = init_login_gen.__next__()
            except Exception as e:
                print(e)
                print("exception worked")
                continue
            browser: Browser = browser
            context: BrowserContext = context
            page: Page = page
            start = time.time()
            curr_url = ""
            try:
                for el in self.queue_iter:
                    is_loaded = False
                    print(el)
                    curr_url = el
                    # todo make save curr_el and re-parse if error by custom error
                    page.set_default_timeout(30000)
                    while True:
                        try:
                            page.goto(el, wait_until="domcontentloaded")
                            print(" page loaded")
                            is_loaded = True
                            break
                        except Exception:
                            print("Page didn't load within the timeout, refreshing...")
                            page.reload()
                            continue
                    print("page loaded")
                    if (time.time() - start) % 50:
                        try:
                            fill_untill_max(self.queue, self.url_iter)
                        except StopIteration as e:
                            raise e
                        except Exception as e:
                            print(e)
            except StopIteration as e:
                print(e)
                break
            except Exception as e:
                print(e)
                return False
        return True


def main(path_to_file: str):
    # get_all_products("https://www.schmalz.com/en-de/sitemap-products.xml")
    QUEUE_ONE_FOR_ALL = Queue(maxsize=50)
    URL_ITER = iter(read_urls_from_csv(path_to_file))
    fill_untill_max(QUEUE_ONE_FOR_ALL, URL_ITER)
    # url = QUEUE_ONE_FOR_ALL.get()
    # print(url)
    # print(type(url))
    print("filled")
    with ProcessPoolExecutor(max_workers=1) as executor:
        parser = playwright_parser(
            QUEUE_ONE_FOR_ALL,
            path_to_file,
            URL_ITER,
        )
        print("before submit")
        # parser.check_get()
        res = executor.submit(parser.start_requests())
        print(res)


main("./product_urls.csv")
