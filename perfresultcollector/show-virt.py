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

(options, args) = optparser.parse_args()

# open DB
db = DBConnection()
qr = Query("virt")


def show_virt(csv, **kwargs):
    head = ["id", "name"]
    for option in kwargs:
        if kwargs[option]:
            qr.filter({option: kwargs[option]})
    for line in get_formatted_data(qr.execute(), csv, head):
        print line


if __name__ == '__main__':
    show_virt(options.csv, name=options.name)
