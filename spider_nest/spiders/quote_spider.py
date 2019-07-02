# -*- coding: utf-8 -*-

import scrapy

from spider_nest.items import QuoteItem
from spider_nest.spider_handler import SpiderHandler


class QuoteSpider(scrapy.Spider, SpiderHandler):

    def __init__(self):

        self.name = 'quote_spider'
        self.allowed_domains = ['toscrape.com']
        self.start_urls = ['http://quotes.toscrape.com/']

        self.url_base = 'http://quotes.toscrape.com/'

        # Limit the pages to scrape
        self.page_limit = 3
        self.current_pages = 0

        SpiderHandler.__init__(self)

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0],
                             callback=self.handle_parse,
                             errback=self.errback_handler)

    def handle_parse(self, response):

        self.increase_request_count()

        try:
            yield from self.parse(response)
        except Exception as e:
            self.exception_handler(e)

    def parse(self, response):

        self.increase_request_count()

        for item in response.xpath('//div[@class="quote"]'):
            yield from self.extract_quote(item)

        self.current_pages += 1
        if self.current_pages >= self.page_limit:
            return

        next_page_url = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(self.url_base + next_page_url,
                                 callback=self.handle_parse,
                                 errback=self.errback_handler)

    def extract_quote(self, item):

        quote = QuoteItem()
        quote['text'] = item.xpath('.//span[@class="text"]/text()').extract_first()[1:-1]
        quote['author'] = item.xpath('.//span/small[@class="author"]/text()').extract_first()
        quote['tags'] = ', '.join(item.xpath('.//div[@class="tags"]/a/text()').extract())

        self.increase_item_count()

        yield quote
