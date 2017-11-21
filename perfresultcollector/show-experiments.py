#!/usr/bin/env python

import argparse

from format_data import get_formatted_data
from models import Query

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--name", action="store", dest="name")
parser.add_argument("--csv", action="store_true", default=False, dest="csv")
parser.add_argument("--table", action="store_true", default=False, dest="table")

options = parser.parse_args()

qr = Query("experiments")


def show_experiment(csv, table, **kwargs):
    head = ["id", "cmd", "description", "systemwide"]
    for key, value in kwargs.items():
        if value:
            qr.filter({key: value})
    data = qr.execute()
    for line in get_formatted_data(data, csv, head, table):
        print line


if __name__ == '__main__':
    show_experiment(options.csv, options.table, name=options.name)
