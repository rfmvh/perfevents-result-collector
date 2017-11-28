#!/usr/bin/env python

import argparse

from models import Query
from formatter import format_output

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--arch", action="store", dest="arch")
parser.add_argument("--microarch", action="store", dest="microarch")
parser.add_argument("--family", action="store", dest="family")
parser.add_argument("--model", action="store", dest="model")
parser.add_argument("--stepping", action="store", dest="stepping")
parser.add_argument("--virt", action="store", dest="virt")
parser.add_argument("--kernel", action="store", dest="kernel")
parser.add_argument("--vendor", action="store", dest="vendor")
parser.add_argument("--debug", action="store_true", default=False, dest="debug")
parser.add_argument("--csv", action="store_true", default=False, dest="csv")
parser.add_argument("--table", action="store_true", default=False, dest="table")

options = parser.parse_args()


def show_environment(csv, table, debug, **kwargs):
    qr = Query("environments")
    qr.set_select("env_id", "arch", "microarch", "family", "model", "stepping",
                  "virt.name", "kernels.name", "vendors.name")
    for key, value in kwargs.items():
        if value:
            qr.filter({key: value})
    head = qr.get_select().split(", ")
    if debug:
        print qr.execute(debug=debug)
    else:
        data = qr.execute()
        for line in format_output(data, csv, head, table):
            print line


if __name__ == '__main__':
    show_environment(options.csv, options.table, options.debug, arch=options.arch, microarch=options.microarch,
                     family=options.family,
                     model=options.model, stepping=options.stepping, virt__name=options.virt,
                     kernels__name=options.kernel, vendors__name=options.vendor)