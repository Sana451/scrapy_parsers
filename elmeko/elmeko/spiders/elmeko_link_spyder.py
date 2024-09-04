import csv

import scrapy

ERROR_FILE_NAME = "/home/sana451/PycharmProjects/scrapy_norelem/parsers/elmeko/elmeko/elmeko_link_errors.csv"


def save_error(url, error, err_file_path=ERROR_FILE_NAME):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, type(error), error])


class LinksSpider(scrapy.Spider):
    name = "elmeko_link"

    custom_settings = {
        "CONCURRENT_REQUESTS": 8,
        "RETRY_TIMES": 3,
        "DUPEFILTER_DEBUG": True,
        "ROBOTSTXT_OBEY": False,
        # "DOWNLOAD_DELAY": 20,
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en",
        },
        # "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        # "DOWNLOAD_HANDLERS": {
        #     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        #     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        # },

    }

    def start_requests(self):
        urls = [
            "https://www.elmeko.de/en/products/",
        ]
        for url in urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_main_category_links,
                                 errback=self.errback, )

    def errback(self, failure):
        save_error(failure.request.url, failure)

    def parse_main_category_links(self, response):

        try:
            main_category_links = [a.attrib['href'] for a in response.css('.card-deck a')]
        except Exception as error:
            save_error(response.url, error)

        if main_category_links:
            for m_c_link in main_category_links:
                yield scrapy.Request(m_c_link, callback=self.parse_category_links)

    def parse_category_links(self, response):
        try:
            category_links = [a.attrib['href'] for a in response.css('.card-deck a')]
        except Exception as error:
            save_error(response.url, error)

        if category_links:
            for c_link in category_links:
                yield scrapy.Request(c_link, callback=self.parse_links)


    def parse_links(self, response):
        try:
            product_links = [a.attrib['href'] for a in response.css('a.product-item-link')]
        except Exception as error:
            save_error(response.url, error)

        for product_link in product_links:
            yield {"url": product_link}