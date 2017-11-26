#!/usr/bin/env python

import argparse

from tools import format_output
from models import Query

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--name", action="store", dest="name")
parser.add_argument("--csv", action="store_true", default=False, dest="csv")
parser.add_argument("--table", action="store_true", default=False, dest="table")

options = parser.parse_args()


def show_experiment(csv, table, **kwargs):
    qr = Query("experiments")
    head = ["id", "cmd", "description", "systemwide"]
    for key, value in kwargs.items():
        if value:
            qr.filter({key: value})
    data = qr.execute()
    for line in format_output(data, csv, head, table):
        print line


if __name__ == '__main__':
    show_experiment(options.csv, options.table, name=options.name)
