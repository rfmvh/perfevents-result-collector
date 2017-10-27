#!/usr/bin/env python

from dbinterface import *
from optparse import OptionParser
from models import Query
from format_data import type_of_log

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--arch", action="store", dest="arch")
optparser.add_option("", "--microarch", action="store", dest="microarch")
optparser.add_option("", "--family", action="store", dest="family")
optparser.add_option("", "--model", action="store", dest="model")
optparser.add_option("", "--stepping", action="store", dest="stepping")
optparser.add_option("", "--virt", action="store", dest="virt")
optparser.add_option("", "--kernel", action="store", dest="kernel")
optparser.add_option("", "--vendor", action="store", dest="vendor")
optparser.add_option("", "--csv", action="store_true", default=False, dest="csv")
optparser.add_option("", "--table", action="store_true", default=False, dest="table")

(options, args) = optparser.parse_args()

# open DB
db = DBConnection()
qr = Query("environments")
qr.set_select("env_id", "arch", "microarch", "family", "model", "stepping",
              "virt.name", "kernels.name", "vendors.name")


def show_environment(csv, table, **kwargs):
    for option in kwargs:
        if kwargs[option]:
            qr.filter({option: kwargs[option]})
    head = qr.get_select().split(", ")
    data = qr.execute()
    if table:
        output_data = type_of_log(data, csv, head, table)
        widths = [max(map(len, col)) for col in zip(*output_data)]
        for row in output_data:
            print " | ".join((val.ljust(width) for val, width in zip(row, widths)))
    else:
        for line in type_of_log(data, csv, head):
            print line


if __name__ == '__main__':
    show_environment(options.csv, options.table, arch=options.arch, microarch=options.microarch, family=options.family,
                     model=options.model, stepping=options.stepping, virt__name=options.virt,
                     kernel__name=options.kernel, vendors__name=options.vendor)
