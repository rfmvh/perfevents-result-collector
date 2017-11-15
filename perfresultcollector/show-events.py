#!/usr/bin/env python

import argparse

from format_data import get_formatted_data
from models import Query

parser = argparse.ArgumentParser()

parser.set_defaults(listmode=0)
parser.add_argument("--name", action="store", dest="name")
parser.add_argument("--idgroup", action="store", dest="idGroup")
parser.add_argument("--csv", action="store_true", default=False, dest="csv")
parser.add_argument("--table", action="store_true", default=False, dest="table")
options = parser.parse_args()

# open DB
qr = Query("events")


def show_event(csv, table, **kwargs):
    for option in kwargs:
        if kwargs[option]:
            qr.filter({option: kwargs[option]})
    head = ["id", "name", "evt_num", "nmas", "idGroup"]
    data = qr.execute()
    for line in get_formatted_data(data, csv, head, table):
        print line


if __name__ == '__main__':
    show_event(options.csv, options.table, name=options.name, idGroup=options.idGroup)
