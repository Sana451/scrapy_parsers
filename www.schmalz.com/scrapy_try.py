import scrapy


class SchmalzSpider(scrapy.Spider):
    name = "schmalz"
    start_urls = ["https://www.schmalz.com/en-de/"]

    def parse(self, response):
        # Find all elements with the "clearfix" class
        clearfix_elements = response.css(".clearfix")

        # Extract the href links from each clearfix element
        for element in clearfix_elements:
            links = element.css("a::attr(href)").getall()
            for link in links:
                yield {"link": "https://www.schmalz.com/en-de/" + link}
