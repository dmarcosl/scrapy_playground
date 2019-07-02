# -*- coding: utf-8 -*-

from multiprocessing import Process

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from spider_nest import settings
from spider_nest.spiders.book_spider import BookSpider
from spider_nest.spiders.quote_spider import QuoteSpider


def execute_spiders_synchronous():
    """ Execute the spiders and wait for them to finish """

    execute_spiders()


def execute_spiders_asynchronous():
    """ Execute the spiders without wait for them to finish """

    process = Process(target=execute_spiders)
    process.start()


def execute_spiders():
    """ Execute the spiders """

    # Set the crawler settings
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # Initialize the crawler process and add the spiders
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(BookSpider)
    crawler_process.crawl(QuoteSpider)

    # Start the process and close it at finish
    crawler_process.start()
    crawler_process.stop()


if __name__ == '__main__':
    execute_spiders_synchronous()
    # execute_spiders_asynchronous()
