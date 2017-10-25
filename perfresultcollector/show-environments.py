#!/usr/bin/env python

from dbinterface import *
from optparse import OptionParser
from models import Query
from extra import type_of_log

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

(options, args) = optparser.parse_args()

# open DB
db = DBConnection()
qr = Query("environments")
qr.set_select("env_id", "arch", "microarch", "family", "model", "stepping",
              "virt.name", "kernels.name", "vendors.name")


def show_environment(csv, **options):
    for option in options:
        if options[option]:
            qr.filter({option: options[option]})
    data = qr.execute()
    head = qr.get_select().split(", ")
    for line in type_of_log(data, csv, head):
        print line


show_environment(options.csv, arch=options.arch, microarch=options.microarch, family=options.family,
                 model=options.model, stepping=options.stepping, virt=options.virt,
                 kernel=options.kernel, vendor=options.vendor)
