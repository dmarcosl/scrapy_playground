# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spider_nest.exporter import Exporter


class SpiderNestPipeline(object):

    def open_spider(self, spider):
        self.exporter = Exporter()

    def process_item(self, item, spider):
        if not self.exporter.is_started():
            self.exporter.start(spider.name, list(item.__dict__.get('_values').keys()))
        self.exporter.add_row(item.__dict__.get('_values'))

        return item

    def close_spider(self, spider):
        spider.set_end_time()

        if self.exporter.is_started():
            self.exporter.close()

        print('Requests: {}'.format(spider.request_count))
        print('Items: {}'.format(spider.item_count))
        print('Execution time: {}ms'.format(spider.get_execution_time()))
