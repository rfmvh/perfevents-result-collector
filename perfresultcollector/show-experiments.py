#!/usr/bin/env python

import sys
import re
import os

from dbinterface import *
from optparse import OptionParser
from models import Query
from format_data import get_formatted_data

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--name", action="store", dest="name")
optparser.add_option("", "--csv", action="store_true", default=False, dest="csv")
optparser.add_option("", "--table", action="store_true", default=False, dest="table")

(options, args) = optparser.parse_args()

# open DB
db = DBConnection()
qr = Query("experiments")


def show_experiment(csv, table, **kwargs):
    head = ["id", "cmd", "description", "systemwide"]
    for option in kwargs:
        if kwargs[option]:
            qr.filter({option: kwargs[option]})
    data = qr.execute()
    for line in get_formatted_data(data, csv, head, table):
        print line


if __name__ == '__main__':
    show_experiment(options.csv, options.table, name=options.name)
