#!/usr/bin/env python

import sys
import re
import os

from dbinterface import *
from optparse import OptionParser
from models import Query
from extra import type_of_log

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--name", action="store", dest="name")
optparser.add_option("", "--csv", action="store_true", default=False, dest="csv")
optparser.add_option("", "--table", action="store_true", default=False, dest="table")

(options, args) = optparser.parse_args()

# open DB
db = DBConnection()
qr = Query("experiments")


def show_experiment(csv, table, **options):
    head = ["id", "cmd", "description", "systemwide"]
    for option in options:
        if options[option]:
            qr.filter({option: options[option]})
    data = qr.execute()
    if table:
        output_data = type_of_log(data, csv, head, table)
        widths = [max(map(len, col)) for col in zip(*output_data)]
        for row in output_data:
            print " | ".join((val.ljust(width) for val, width in zip(row, widths)))
    else:
        for line in type_of_log(data, csv, head):
            print line

show_experiment(options.csv, options.table, name=options.name)
