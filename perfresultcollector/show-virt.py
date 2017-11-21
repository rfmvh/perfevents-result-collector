#!/usr/bin/env python

import argparse

from format_data import get_formatted_data
from models import Query

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--name", action="store", dest="name")
parser.add_argument("--csv", action="store_true", default=False, dest="csv")

options = parser.parse_args()

qr = Query("virt")


def show_virt(csv, **kwargs):
    head = ["id", "name"]
    for key, value in kwargs.items():
        if value:
            qr.filter({key: value})
    for line in get_formatted_data(qr.execute(), csv, head):
        print line


if __name__ == '__main__':
    show_virt(options.csv, name=options.name)
