#!/usr/bin/env python

import argparse

from perfresultcollector.formatter import format_output
from perfresultcollector.models import Query


parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--name", action="store")
parser.add_argument("--version", action="store")
parser.add_argument("--csv", action="store_true", default=False)
parser.add_argument("--table", action="store_true", default=False)
parser.add_argument("--debug", action="store_true", default=False)

options = parser.parse_args()


def show_tool(csv, table, debug, **kwargs):
    qr = Query("tools")
    for key, value in kwargs.items():
        if value:
            qr.filter(**{key: value})
    head = ["id", "evt_num", "nmas", "idGroup"]
    if debug:
        print qr.execute(debug=debug)
    else:
        data = qr.execute()
        for line in format_output(data, csv, head, table):
            print line


if __name__ == '__main__':
    show_tool(options.csv, options.table, options.debug, name=options.name, version=options.version)

