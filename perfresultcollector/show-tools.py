#!/usr/bin/env python

import argparse

from format_data import get_formatted_data
from models import Query

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--name", action="store", dest="name")
parser.add_argument("--version", action="store", dest="version")
parser.add_argument("--csv", action="store_true", default=False, dest="csv")
parser.add_argument("--table", action="store_true", default=False, dest="table")

options = parser.parse_args()


def show_tool(csv, table, **kwargs):
    qr = Query("tools")
    for key, value in kwargs.items():
        if value:
            qr.filter({key: value})
    head = ["id", "evt_num", "nmas", "idGroup"]
    data = qr.execute()
    for line in get_formatted_data(data, csv, head, table):
        print line


if __name__ == '__main__':
    show_tool(options.csv, options.table, name=options.name, version=options.version)
