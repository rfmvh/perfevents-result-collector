#!/usr/bin/env python

# TODO add details
# TODO recreate strucutre about heading
import sys
import re
import os

from dbinterface import *
from optparse import OptionParser
from models import Query
from extra import type_of_log

optparser = OptionParser()
optparser.set_defaults(listmode=0)
optparser.add_option("", "--event", action="store", dest="event", help="name event")
optparser.add_option("", "--event-group", action="store", dest="eventGroup")
optparser.add_option("", "--tool-name", action="store", dest="toolName")
optparser.add_option("", "--tool-version", action="store", dest="toolVersion")
optparser.add_option("", "--experiment", action="store", dest="experiment")
optparser.add_option("", "--cpu-family", action="store", dest="family")
optparser.add_option("", "--cpu-model", action="store", dest="model")
optparser.add_option("", "--cpu-vendor", action="store", dest="vendor")
optparser.add_option("", "--cpu-arch", action="store", dest="arch")
optparser.add_option("", "--cpu-microarch", action="store", dest="microarch")
optparser.add_option("", "--kernel", action="store", dest="kernel")
optparser.add_option("", "--virt", action="store", dest="virt")

optparser.add_option("", "--event-details", action="store_true", default=False, dest="eventD")
optparser.add_option("", "--tool-details", action="store_true", default=False, dest="toolD")
optparser.add_option("", "--experiment-details", action="store_true", default=False, dest="expD")
optparser.add_option("", "--env-details", action="store", dest="envD",
                     help="1 = arch, microarch; 2=arch, microarch, family, model")
optparser.add_option("", "--kernel-details", action="store_true", default=False, dest="kernelD")
optparser.add_option("", "--virt-details", action="store_true", default=False, dest="virtD")

optparser.add_option("", "--csv", action="store_true", default=False, dest="csv")
optparser.add_option("", "--table", action="store_true", default=False, dest="table")

(options, args) = optparser.parse_args()

# open DB
db = DBConnection()
qr = Query("results")
qr.set_select("results.val", "events.name", "events.evt_num", "events.nmask", "events.idgroup",
              "tools.name, tools.version", "experiments.name",
              "environments.arch", "environments.microarch", " environments.family", "environments.model",
              "kernels.name", "virt.name")


def show_result(csv, table, **options):
    for option in options:
        if options[option]:
            qr.filter({option: options[option]})
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

show_result(options.csv, options.table, events__name=options.event, events__idgroup=options.eventGroup,
            tools__name=options.toolName,
            tools__version=options.toolVersion, experiments__name=options.experiment,
            environments__family=options.family, environments__model=options.model, vendors__name=options.vendor,
            environments__arch=options.arch, environments__microarch=options.microarch, kernels__name=options.kernel,
            virt__name=options.virt)
