# -*- coding: utf-8 -*-

import csv
import os


class Exporter:

    def __init__(self):
        self.csvfile = None
        self.writer = None

    def is_started(self):
        """ Check if the exporter is initialized

        :return: Boolean indicating is initialized
        """

        return bool(self.csvfile)

    def start(self, name, headers):
        """ Initialize the CSV file

        :param name: Name of the file
        :param headers: List of headers of the CSV file
        """

        # Root project directory
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, '..', name + '.csv')

        self.csvfile = open(path, 'w', encoding='utf-8')
        self.writer = csv.DictWriter(self.csvfile, fieldnames=headers)
        self.writer.writeheader()

    def add_row(self, row):
        """ Add a row to the CSV file

        :param row: Dictionary with headers as keys and values as item values
        """

        self.writer.writerow(row)

    def close(self):
        """ Close the CSV file """

        self.csvfile.close()
