#!/usr/bin/env python

import argparse

from formatter import format_output
from models import Query

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--name", action="store")
parser.add_argument("--csv", action="store_true", default=False)
parser.add_argument("--debug", action="store_true", default=False)

options = parser.parse_args()


def show_vendor(csv, debug, **kwargs):
    qr = Query("vendors")
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
    show_vendor(options.csv, options.debug, name=options.name)
