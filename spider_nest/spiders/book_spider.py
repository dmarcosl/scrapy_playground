# -*- coding: utf-8 -*-

import scrapy

from spider_nest.items import BookItem
from spider_nest.spider_handler import SpiderHandler


class BookSpider(scrapy.Spider, SpiderHandler):

    def __init__(self):

        self.name = 'book_spider'
        self.allowed_domains = ['toscrape.com']
        self.start_urls = ['http://books.toscrape.com']

        self.url_base = 'http://books.toscrape.com/'
        self.url_catalogue_base = 'http://books.toscrape.com/catalogue/'

        # Limit the pages to scrape
        self.page_limit = 2
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

        for item_url in response.xpath('//div[@class="image_container"]/a/@href').extract():
            if 'catalogue' in item_url:
                url = self.url_base + item_url
            else:
                url = self.url_catalogue_base + item_url

            yield scrapy.Request(url,
                                 callback=self.handle_extract_book,
                                 errback=self.errback_handler)

        self.current_pages += 1
        if self.current_pages >= self.page_limit:
            return

        next_page_url = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').extract_first()
        if next_page_url:
            if 'catalogue' in next_page_url:
                url = self.url_base + next_page_url
            else:
                url = self.url_catalogue_base + next_page_url

            yield scrapy.Request(url,
                                 callback=self.handle_parse,
                                 errback=self.errback_handler)

    def handle_extract_book(self, response):

        self.increase_request_count()

        try:
            yield from self.extract_book(response)
        except Exception as e:
            self.exception_handler(e)

    def extract_book(self, response):

        book = BookItem()

        title_block = response.xpath('//article[@class="product_page"]/div/div[contains(@class, "product_main")]')
        book['title'] = title_block.xpath('.//h1/text()').extract_first()
        book['rating'] = title_block.xpath('.//p[contains(@class, "star-rating")]/@class').extract_first() \
            .split(' ')[-1]

        book['description'] = response.xpath('//article[@class="product_page"]/p[1]/text()').extract_first()

        table_items = response.xpath('//article[@class="product_page"]/table/tr/td/text()').extract()
        book['upc'] = table_items[0]
        book['type'] = table_items[1]
        book['price_excl_tax'] = table_items[2][1:]
        book['price_incl_tax'] = table_items[3][1:]
        book['tax'] = table_items[4][1:]
        book['availability'] = table_items[5]
        book['reviews'] = table_items[6]

        self.increase_item_count()

        yield book
