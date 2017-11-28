#!/usr/bin/env python

import argparse

from models import Query
from formatter import format_output

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--name", action="store", dest="name")
parser.add_argument("--csv", action="store_true", default=False, dest="csv")
parser.add_argument("--debug", action="store_true", default=False, dest="debug")

options = parser.parse_args()


def show_virt(csv, debug, **kwargs):
    qr = Query("virt")
    head = ["id", "name"]
    for key, value in kwargs.items():
        if value:
            qr.filter(**{key: value})
    if debug:
        print qr.execute(debug=debug)
    else:
        data = qr.execute()
        for line in format_output(data, csv, head):
            print line


if __name__ == '__main__':
    show_virt(options.csv, options.debug, name=options.name)
