# -*- coding: utf-8 -*-

import logging
import sys
import time
import traceback

from scrapy.exceptions import IgnoreRequest


class SpiderHandler:

    def __init__(self):
        self.request_count = 0
        self.item_count = 0
        self.start_time = self.end_time = get_current_millis()

        # Error specific variables
        self.error_msg_sent = False
        self.continue_requesting = True

    def increase_request_count(self, quantity=1):
        self.request_count += quantity

    def increase_item_count(self, quantity=1):
        self.item_count += quantity

    def set_end_time(self):
        self.end_time = get_current_millis()

    def get_execution_time(self):
        return self.end_time - self.start_time

    def exception_handler(self, exception):
        """ Method to control code errors in the spiders, produced by changes in the websites, like
        'Index out of bound', 'null pointer', etc

        :param exception: Instance of the error
        """

        if not self.error_msg_sent:
            ex_type, ex, tb = sys.exc_info()

            msg = 'Error Message: ' + str(exception)
            msg += '\nTraces:\n' + '\n'.join([str(trace) for trace in traceback.extract_tb(tb)])

            logging.error(msg)

            self.error_msg_sent = True

        self.continue_requesting = False

    def errback_handler(self, failure):
        """ Method to control errors in the Scrapy requests

        :param failure: Instance of the failure
        """

        if not failure.type == IgnoreRequest and not self.error_msg_sent:
            msg = 'Error Message: ' + failure.getErrorMessage()
            msg += '\nUrl: ' + failure.request.url
            msg += '\nHTTP method: ' + failure.request.method
            msg += '\nTraces:\n' + failure.getTraceback()

            logging.error(msg)

            self.error_msg_sent = True

        self.continue_requesting = False


def get_current_millis():
    """ Obtain the current milliseconds

    :return: Current milliseconds
    """

    return int(round(time.time() * 1000))
