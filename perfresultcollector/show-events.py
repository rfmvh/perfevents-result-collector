#!/usr/bin/env python

import sys
import re
import os

from optparse import OptionParser
from models import Query
from format_data import get_formatted_data

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--name", action="store", dest="name")
optparser.add_option("", "--idgroup", action="store", dest="idGroup")
optparser.add_option("", "--csv", action="store_true", default=False, dest="csv")
optparser.add_option("", "--table", action="store_true", default=False, dest="table")
(options, args) = optparser.parse_args()

# open DB
qr = Query("events")

def show_event(csv, table, **kwargs):
    for option in kwargs:
        if kwargs[option]:
            qr.filter({option: kwargs[option]})
    head = ["id","name", "evt_num", "nmas", "idGroup"]
    data = qr.execute()
    for line in get_formatted_data(data, csv, head, table):
        print line

if __name__ == '__main__':
    show_event(options.csv, options.table, name=options.name, idGroup=options.idGroup)
