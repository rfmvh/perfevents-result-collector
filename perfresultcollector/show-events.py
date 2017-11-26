#!/usr/bin/env python

import argparse

from models import Query
from tools import format_output

parser = argparse.ArgumentParser()

parser.set_defaults(listmode=0)
parser.add_argument("--name", action="store", dest="name")
parser.add_argument("--idgroup", action="store", dest="idGroup")
parser.add_argument("--debug", action="store_true", default=False, dest="debug")
parser.add_argument("--csv", action="store_true", default=False, dest="csv")
parser.add_argument("--table", action="store_true", default=False, dest="table")
options = parser.parse_args()


# open DB


def show_event(csv, table, debug, **kwargs):
    qr = Query("events")
    for key, value in kwargs.items():
        if value:
            qr.filter({key: value})
    head = ["id", "name", "evt_num", "nmas", "idGroup"]
    if debug:
        print qr.execute(debug=debug)
    else:
        data = qr.execute(debug=debug)
        for line in format_output(data, csv, head, table):
            print line


if __name__ == '__main__':
    show_event(options.csv, options.table, options.debug, name=options.name, idGroup=options.idGroup)
