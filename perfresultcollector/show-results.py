#!/usr/bin/env python

import argparse

from . import format_output
from models import Query

parser = argparse.ArgumentParser()
parser.set_defaults(listmode=0)
parser.add_argument("--event", action="store", dest="event", help="name event")
parser.add_argument("--event-group", action="store", dest="eventGroup")
parser.add_argument("--tool-name", action="store", dest="toolName")
parser.add_argument("--tool-version", action="store", dest="toolVersion")
parser.add_argument("--experiment", action="store", dest="experiment")
parser.add_argument("--cpu-family", action="store", dest="family")
parser.add_argument("--cpu-model", action="store", dest="model")
parser.add_argument("--cpu-vendor", action="store", dest="vendor")
parser.add_argument("--cpu-arch", action="store", dest="arch")
parser.add_argument("--cpu-microarch", action="store", dest="microarch")
parser.add_argument("--kernel", action="store", dest="kernel")
parser.add_argument("--virt", action="store", dest="virt")

parser.add_argument("--event-details", action="store_true", default=False, dest="eventD")
parser.add_argument("--tool-details", action="store_true", default=False, dest="toolD")
parser.add_argument("--experiment-details", action="store_true", default=False, dest="expD")
parser.add_argument("--env-details", action="store", dest="envD",
                    help="1 = arch, microarch; 2=arch, microarch, family, model")
parser.add_argument("--kernel-details", action="store_true", default=False, dest="kernelD")
parser.add_argument("--virt-details", action="store_true", default=False, dest="virtD")

parser.add_argument("--csv", action="store_true", default=False, dest="csv")
parser.add_argument("--table", action="store_true", default=False, dest="table")

options = parser.parse_args()


def get_select():
    basic_details = {"events.evt_num": options.eventD, "events.nmask": options.eventD, "tools.name": options.toolD,
                     "tools.version": options.toolD, "experiments.name": options.expD,
                     "kernels.name": options.kernelD, "virt.name": options.virtD}
    details = ["results.val", "events.name", "events.idgroup"]
    for index in basic_details:
        if basic_details[index]:
            details.append(index)
    if options.envD == "1":
        details += ["environments.arch", "environments.microarch"]
    elif options.envD == "2":
        details += ["environments.arch", "environments.microarch", "environments.family", "environments.model"]
    return details


def show_result(csv, table, **kwargs):
    qr = Query("results")
    qr.set_select(get_select())
    for key, value in kwargs.items():
        if value:
            qr.filter({key: value})
    head = get_select()
    data = qr.execute()
    for line in format_output(data, csv, head, table):
        print line


if __name__ == '__main__':
    show_result(options.csv, options.table, events__name=options.event, events__idgroup=options.eventGroup,
                tools__name=options.toolName,
                tools__version=options.toolVersion, experiments__name=options.experiment,
                environments__family=options.family, environments__model=options.model, vendors__name=options.vendor,
                environments__arch=options.arch, environments__microarch=options.microarch,
                kernels__name=options.kernel,
                virt__name=options.virt)
