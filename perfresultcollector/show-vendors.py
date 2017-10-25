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

(options, args) = optparser.parse_args()

# open DB
db = DBConnection()
qr = Query("vendors")


def show_vendor(csv, **options):
    head = []
    for option in options:
        if options[option]:
            qr.filter({option: options[option]})
    for line in type_of_log(qr.execute(), csv, head):
        print line


show_vendor(options.csv, name=options.name)
